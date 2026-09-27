#!/usr/bin/env python3
import argparse, hashlib, json, math, statistics, time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

from fish_speech.models.text2semantic.inference import (
    decode_to_audio, encode_audio, generate_long, init_model, load_codec_model
)

TEXT_CASES = [
 {"id":"B01-en-short","language":"en","length":"short","text":"Hello. This is the short English benchmark for Fish Audio S2 Pro.","max_new_tokens":160},
 {"id":"B02-vi-short","language":"vi","length":"short","text":"Xin chào. Đây là bài benchmark tiếng Việt ngắn cho Fish Audio S2 Pro.","max_new_tokens":160},
 {"id":"B03-en-medium","language":"en","length":"medium","text":"This controlled benchmark measures warm inference latency, real time factor, and GPU memory on the dual NVIDIA T4 pipeline. The semantic model runs on the first GPU and the codec decoder runs on the second GPU.","max_new_tokens":320},
 {"id":"B04-vi-medium","language":"vi","length":"medium","text":"Bài benchmark có kiểm soát này đo độ trễ suy luận, hệ số thời gian thực và bộ nhớ GPU trên hệ thống hai NVIDIA T4. Mô hình sinh mã ngữ nghĩa chạy trên GPU thứ nhất và bộ giải mã âm thanh chạy trên GPU thứ hai.","max_new_tokens":320},
 {"id":"B05-en-long","language":"en","length":"long","text":"Fish Audio S2 Pro is being evaluated on a reproducible Kaggle environment with two NVIDIA T4 GPUs. The purpose of this longer English case is to exercise the semantic generation path for a sustained interval while preserving the same precision, context length, sampling parameters, and decoder topology used throughout qualification. We measure wall clock inference time, generated audio duration, real time factor, semantic throughput, and peak memory on both GPUs. This is a controlled engineering benchmark rather than a subjective quality ranking.","max_new_tokens":480},
 {"id":"B06-vi-long","language":"vi","length":"long","text":"Fish Audio S2 Pro đang được đánh giá trong một môi trường Kaggle có thể tái lập với hai GPU NVIDIA T4. Mục tiêu của trường hợp tiếng Việt dài hơn này là duy trì quá trình sinh mã ngữ nghĩa trong một khoảng thời gian đủ lớn, đồng thời giữ nguyên độ chính xác số, độ dài ngữ cảnh, tham số lấy mẫu và cấu trúc bộ giải mã đã dùng trong các giai đoạn kiểm thử trước. Chúng tôi đo thời gian suy luận, thời lượng âm thanh, hệ số thời gian thực, thông lượng sinh mã và mức sử dụng bộ nhớ cao nhất trên cả hai GPU.","max_new_tokens":480},
]

CLONE_CASES = [
 {"id":"B07-clone-en","language":"en","ref_language":"en","text":"This is the warm voice cloning benchmark using the English reference voice.","max_new_tokens":220},
 {"id":"B08-clone-vi","language":"vi","ref_language":"vi","text":"Đây là bài benchmark sao chép giọng nói dùng giọng tham chiếu tiếng Việt.","max_new_tokens":220},
]

REFS = {
 "en": {
   "path":"results/bilingual-text-synthesis/T03-en-medium.wav",
   "text":"Today we are validating a reproducible dual GPU inference pipeline. The semantic model runs on the first NVIDIA T4, while the audio decoder runs on the second T4. The goal is stable, clear speech without running out of GPU memory."
 },
 "vi": {
   "path":"results/bilingual-text-synthesis/T04-vi-medium.wav",
   "text":"Hôm nay chúng tôi kiểm thử một quy trình suy luận hai GPU có thể tái lập. Mô hình sinh mã ngữ nghĩa chạy trên GPU NVIDIA T4 thứ nhất, còn bộ giải mã âm thanh chạy trên GPU T4 thứ hai. Mục tiêu là tạo giọng nói rõ ràng, ổn định và không bị hết bộ nhớ GPU."
 }
}

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def audio_stats(y, sr):
    y=np.asarray(y,dtype=np.float32).reshape(-1)
    a=np.abs(y)
    return {
      "duration_s":float(len(y)/sr),
      "sample_rate":int(sr),
      "peak_abs":float(a.max()) if len(y) else 0.0,
      "rms":float(np.sqrt(np.mean(y*y))) if len(y) else 0.0,
      "silence_ratio_lt_1e-4":float(np.mean(a<1e-4)) if len(y) else 1.0,
      "clipping_ratio_ge_0_999":float(np.mean(a>=0.999)) if len(y) else 0.0,
    }

def one_run(model, decode_one_token, codec, case, sem_dev, dec_dev, seed, prompt_text=None, prompt_tokens=None):
    torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    for i in (0,1): torch.cuda.reset_peak_memory_stats(i)

    wall0=time.perf_counter()
    sem0=time.perf_counter()
    chunks=[]
    gen=generate_long(
      model=model, device=sem_dev, decode_one_token=decode_one_token,
      text=case["text"], num_samples=1, max_new_tokens=case["max_new_tokens"],
      top_p=0.9, top_k=30, temperature=1.0, compile=False,
      iterative_prompt=True, chunk_length=300,
      prompt_text=prompt_text, prompt_tokens=prompt_tokens
    )
    for response in gen:
      if response.action=="sample":
        chunks.append(response.codes)
    torch.cuda.synchronize(0)
    semantic_s=time.perf_counter()-sem0
    if not chunks: raise RuntimeError("no semantic codes")
    codes=torch.cat(chunks,dim=1)

    dec0=time.perf_counter()
    audio=decode_to_audio(codes.to(dec_dev),codec)
    torch.cuda.synchronize(1)
    decode_s=time.perf_counter()-dec0
    wall_s=time.perf_counter()-wall0
    y=audio.detach().cpu().float().numpy()
    am=audio_stats(y,codec.sample_rate)
    return {
      "seed":seed,
      "semantic_time_s":semantic_s,
      "decode_time_s":decode_s,
      "wall_time_s":wall_s,
      "semantic_frames":int(codes.shape[1]),
      "semantic_tokens_per_s":float(codes.shape[1]/semantic_s) if semantic_s else None,
      "rtf":float(wall_s/am["duration_s"]) if am["duration_s"] else math.inf,
      "gpu0_peak_allocated_bytes":int(torch.cuda.max_memory_allocated(0)),
      "gpu0_peak_reserved_bytes":int(torch.cuda.max_memory_reserved(0)),
      "gpu1_peak_allocated_bytes":int(torch.cuda.max_memory_allocated(1)),
      "gpu1_peak_reserved_bytes":int(torch.cuda.max_memory_reserved(1)),
      **am,
      "_audio":y,
    }

def summarize(values):
    return {
      "min":min(values),
      "median":statistics.median(values),
      "max":max(values),
      "mean":statistics.mean(values),
      "std":statistics.pstdev(values),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--checkpoint",required=True)
    ap.add_argument("--output-dir",required=True)
    ap.add_argument("--runs",type=int,default=5)
    ap.add_argument("--warmups",type=int,default=2)
    ap.add_argument("--semantic-device",default="cuda:0")
    ap.add_argument("--decoder-device",default="cuda:1")
    ap.add_argument("--max-seq-len",type=int,default=4096)
    args=ap.parse_args()
    root=Path(args.repo_root); cp=Path(args.checkpoint); out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)

    session0=time.perf_counter()
    t=time.perf_counter()
    model,decode_one_token=init_model(cp,args.semantic_device,torch.float16,compile=False,max_seq_len=args.max_seq_len)
    with torch.device(args.semantic_device):
      model.setup_caches(max_batch_size=1,max_seq_len=model.config.max_seq_len,dtype=next(model.parameters()).dtype)
    model._cache_setup_done=True
    torch.cuda.synchronize(0)
    semantic_load_s=time.perf_counter()-t

    t=time.perf_counter()
    codec=load_codec_model(cp/"codec.pth",args.decoder_device,torch.float16)
    torch.cuda.synchronize(1)
    codec_load_s=time.perf_counter()-t

    ref_tokens={}
    ref_encode={}
    for lang,ref in REFS.items():
      rp=root/ref["path"]
      t=time.perf_counter()
      tok=encode_audio(rp,codec,args.decoder_device).cpu()
      torch.cuda.synchronize(1)
      ref_tokens[lang]=tok
      ref_encode[lang]={"encode_s":time.perf_counter()-t,"vq_shape":list(tok.shape),"sha256":sha256_file(rp)}

    warm_case={"text":"Warm up the dual GPU benchmark.","max_new_tokens":96}
    warmup_results=[]
    for i in range(args.warmups):
      x=one_run(model,decode_one_token,codec,warm_case,args.semantic_device,args.decoder_device,900+i)
      x.pop("_audio",None)
      warmup_results.append(x)
      print("WARMUP",i+1,json.dumps(x))

    scenarios=[]
    all_cases=[(c,None) for c in TEXT_CASES]+[(c,c["ref_language"]) for c in CLONE_CASES]
    for ci,(case,ref_lang) in enumerate(all_cases):
      runs=[]
      prompt_text=[REFS[ref_lang]["text"]] if ref_lang else None
      prompt_tokens=[ref_tokens[ref_lang]] if ref_lang else None
      for ri in range(args.runs):
        x=one_run(model,decode_one_token,codec,case,args.semantic_device,args.decoder_device,1000+ci*100+ri,prompt_text,prompt_tokens)
        if ri==0:
          wav=out/f"{case['id']}-sample.wav"
          sf.write(wav,x["_audio"],codec.sample_rate,subtype="PCM_16")
          sample={"path":str(wav),"bytes":wav.stat().st_size,"sha256":sha256_file(wav)}
        x.pop("_audio",None)
        runs.append(x)
        print("RUN",case["id"],ri+1,json.dumps(x))
      scenario={
        "id":case["id"],
        "language":case["language"],
        "kind":"voice-cloning" if ref_lang else "text-only",
        "length":case.get("length"),
        "reference_language":ref_lang,
        "text":case["text"],
        "max_new_tokens":case["max_new_tokens"],
        "run_count":len(runs),
        "sample_output":sample,
        "wall_time_s":summarize([x["wall_time_s"] for x in runs]),
        "semantic_time_s":summarize([x["semantic_time_s"] for x in runs]),
        "decode_time_s":summarize([x["decode_time_s"] for x in runs]),
        "audio_duration_s":summarize([x["duration_s"] for x in runs]),
        "rtf":summarize([x["rtf"] for x in runs]),
        "semantic_tokens_per_s":summarize([x["semantic_tokens_per_s"] for x in runs]),
        "gpu0_peak_allocated_gb":summarize([x["gpu0_peak_allocated_bytes"]/1e9 for x in runs]),
        "gpu1_peak_allocated_gb":summarize([x["gpu1_peak_allocated_bytes"]/1e9 for x in runs]),
        "runs":runs,
      }
      (out/f"{case['id']}.json").write_text(json.dumps(scenario,indent=2,ensure_ascii=False)+"\n")
      scenarios.append(scenario)
      print("SCENARIO_DONE",case["id"],"median_wall",scenario["wall_time_s"]["median"],"median_rtf",scenario["rtf"]["median"])

    total_s=time.perf_counter()-session0
    summary={
      "status":"PASS",
      "precision":"FP16","batch_size":1,"compile":False,"max_seq_len":args.max_seq_len,
      "semantic_device":args.semantic_device,"decoder_device":args.decoder_device,
      "semantic_load_s":semantic_load_s,"codec_load_s":codec_load_s,
      "cold_model_ready_s":semantic_load_s+codec_load_s,
      "warmup_count":args.warmups,"runs_per_scenario":args.runs,
      "reference_encode":ref_encode,"warmups":warmup_results,
      "scenario_count":len(scenarios),"total_benchmark_session_s":total_s,
      "scenarios":scenarios
    }
    (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    print("CONTROLLED_BENCHMARK=PASS")

if __name__=="__main__":
    main()
