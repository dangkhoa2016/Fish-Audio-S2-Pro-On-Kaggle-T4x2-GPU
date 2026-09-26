#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

from fish_speech.models.text2semantic.inference import (
    decode_to_audio,
    generate_long,
    init_model,
    load_codec_model,
)

CASES = [
    {
        "id": "T01-en-short",
        "language": "en",
        "category": "short",
        "text": "Hello. This is a short English speech synthesis test for Fish Audio S2 Pro.",
        "max_new_tokens": 160,
    },
    {
        "id": "T02-vi-short",
        "language": "vi",
        "category": "short",
        "text": "Xin chào. Đây là bài kiểm thử tổng hợp giọng nói tiếng Việt ngắn cho Fish Audio S2 Pro.",
        "max_new_tokens": 160,
    },
    {
        "id": "T03-en-medium",
        "language": "en",
        "category": "medium",
        "text": "Today we are validating a reproducible dual GPU inference pipeline. The semantic model runs on the first NVIDIA T4, while the audio decoder runs on the second T4. The goal is stable, clear speech without running out of GPU memory.",
        "max_new_tokens": 320,
    },
    {
        "id": "T04-vi-medium",
        "language": "vi",
        "category": "medium",
        "text": "Hôm nay chúng tôi kiểm thử một quy trình suy luận hai GPU có thể tái lập. Mô hình sinh mã ngữ nghĩa chạy trên GPU NVIDIA T4 thứ nhất, còn bộ giải mã âm thanh chạy trên GPU T4 thứ hai. Mục tiêu là tạo giọng nói rõ ràng, ổn định và không bị hết bộ nhớ GPU.",
        "max_new_tokens": 320,
    },
    {
        "id": "T05-en-expressive",
        "language": "en",
        "category": "expressive",
        "text": "What a wonderful surprise! I did not expect the experiment to work this smoothly. Now, please slow down for a moment... and then finish with confidence: the dual GPU pipeline is working.",
        "max_new_tokens": 280,
    },
    {
        "id": "T06-vi-expressive",
        "language": "vi",
        "category": "expressive",
        "text": "Thật là một bất ngờ tuyệt vời! Tôi không nghĩ thử nghiệm lại diễn ra suôn sẻ đến vậy. Bây giờ, hãy chậm lại một chút... rồi kết thúc thật tự tin: quy trình hai GPU đang hoạt động tốt.",
        "max_new_tokens": 280,
    },
]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def audio_metrics(path: Path):
    y, sr = sf.read(path, dtype="float32", always_2d=False)
    if y.ndim > 1:
        y = y.mean(axis=1)
    abs_y = np.abs(y)
    peak = float(abs_y.max()) if y.size else 0.0
    rms = float(np.sqrt(np.mean(np.square(y)))) if y.size else 0.0
    silence_ratio = float(np.mean(abs_y < 1e-4)) if y.size else 1.0
    clipping_ratio = float(np.mean(abs_y >= 0.999)) if y.size else 0.0
    duration = float(len(y) / sr) if sr else 0.0
    return {
        "sample_rate": int(sr),
        "channels": 1,
        "frames": int(len(y)),
        "duration_s": duration,
        "peak_abs": peak,
        "rms": rms,
        "silence_ratio_lt_1e-4": silence_ratio,
        "clipping_ratio_ge_0_999": clipping_ratio,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--semantic-device", default="cuda:0")
    ap.add_argument("--decoder-device", default="cuda:1")
    ap.add_argument("--max-seq-len", type=int, default=4096)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = Path(args.checkpoint)

    assert torch.cuda.is_available()
    assert torch.cuda.device_count() >= 2

    precision = torch.float16

    print("BILINGUAL_TTS_LOAD_SEMANTIC_BEGIN")
    load_t0 = time.perf_counter()
    model, decode_one_token = init_model(
        checkpoint, args.semantic_device, precision,
        compile=False, max_seq_len=args.max_seq_len,
    )
    with torch.device(args.semantic_device):
        model.setup_caches(
            max_batch_size=1,
            max_seq_len=model.config.max_seq_len,
            dtype=next(model.parameters()).dtype,
        )
    model._cache_setup_done = True
    torch.cuda.synchronize(0)
    semantic_load_s = time.perf_counter() - load_t0
    print(f"BILINGUAL_TTS_SEMANTIC_LOAD_S={semantic_load_s:.3f}")

    print("BILINGUAL_TTS_LOAD_CODEC_BEGIN")
    codec_t0 = time.perf_counter()
    codec = load_codec_model(checkpoint / "codec.pth", args.decoder_device, precision)
    torch.cuda.synchronize(1)
    codec_load_s = time.perf_counter() - codec_t0
    print(f"BILINGUAL_TTS_CODEC_LOAD_S={codec_load_s:.3f}")

    results = []
    for idx, case in enumerate(CASES):
        print(f"CASE_BEGIN={case['id']}")
        torch.manual_seed(args.seed + idx)
        torch.cuda.manual_seed_all(args.seed + idx)
        for gpu in (0, 1):
            torch.cuda.reset_peak_memory_stats(gpu)

        semantic_t0 = time.perf_counter()
        chunks = []
        gen = generate_long(
            model=model,
            device=args.semantic_device,
            decode_one_token=decode_one_token,
            text=case["text"],
            num_samples=1,
            max_new_tokens=case["max_new_tokens"],
            top_p=0.9,
            top_k=30,
            temperature=1.0,
            compile=False,
            iterative_prompt=True,
            chunk_length=300,
            prompt_text=None,
            prompt_tokens=None,
        )
        for response in gen:
            if response.action == "sample":
                chunks.append(response.codes)
        torch.cuda.synchronize(0)
        semantic_s = time.perf_counter() - semantic_t0
        if not chunks:
            raise RuntimeError(f"No semantic codes generated for {case['id']}")
        codes = torch.cat(chunks, dim=1)

        decode_t0 = time.perf_counter()
        audio = decode_to_audio(codes.to(args.decoder_device), codec)
        torch.cuda.synchronize(1)
        decode_s = time.perf_counter() - decode_t0

        wav_path = out_dir / f"{case['id']}.wav"
        sf.write(wav_path, audio.detach().cpu().float().numpy(), codec.sample_rate, subtype="PCM_16")
        metrics = audio_metrics(wav_path)
        total_s = semantic_s + decode_s
        rtf = total_s / metrics["duration_s"] if metrics["duration_s"] > 0 else math.inf

        item = {
            **case,
            "status": "PASS",
            "seed": args.seed + idx,
            "semantic_device": args.semantic_device,
            "decoder_device": args.decoder_device,
            "precision": "FP16",
            "max_seq_len": args.max_seq_len,
            "semantic_codes_shape": list(codes.shape),
            "semantic_time_s": semantic_s,
            "decode_time_s": decode_s,
            "total_inference_s": total_s,
            "rtf": rtf,
            "wav": str(wav_path),
            "wav_bytes": wav_path.stat().st_size,
            "wav_sha256": sha256_file(wav_path),
            "gpu0_peak_allocated_bytes": torch.cuda.max_memory_allocated(0),
            "gpu0_peak_reserved_bytes": torch.cuda.max_memory_reserved(0),
            "gpu1_peak_allocated_bytes": torch.cuda.max_memory_allocated(1),
            "gpu1_peak_reserved_bytes": torch.cuda.max_memory_reserved(1),
            **metrics,
        }
        results.append(item)
        (out_dir / f"{case['id']}.json").write_text(json.dumps(item, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(item, ensure_ascii=False))
        print(f"CASE_END={case['id']}")

    summary = {
        "status": "PASS" if len(results) == len(CASES) and all(x["status"] == "PASS" for x in results) else "FAIL",
        "semantic_load_s": semantic_load_s,
        "codec_load_s": codec_load_s,
        "semantic_device": args.semantic_device,
        "decoder_device": args.decoder_device,
        "precision": "FP16",
        "max_seq_len": args.max_seq_len,
        "case_count": len(results),
        "cases": results,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(f"BILINGUAL_TEXT_SYNTHESIS={summary['status']}")

if __name__ == "__main__":
    main()
