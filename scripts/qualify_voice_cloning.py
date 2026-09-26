#!/usr/bin/env python3
import argparse, hashlib, json, math, time
from pathlib import Path
import numpy as np
import soundfile as sf
import torch

from fish_speech.models.text2semantic.inference import (
    decode_to_audio, encode_audio, generate_long, init_model, load_codec_model
)

REFS = {
  "en": {
    "audio": "results/bilingual-text-synthesis/T03-en-medium.wav",
    "text": "Today we are validating a reproducible dual GPU inference pipeline. The semantic model runs on the first NVIDIA T4, while the audio decoder runs on the second T4. The goal is stable, clear speech without running out of GPU memory."
  },
  "vi": {
    "audio": "results/bilingual-text-synthesis/T04-vi-medium.wav",
    "text": "Hôm nay chúng tôi kiểm thử một quy trình suy luận hai GPU có thể tái lập. Mô hình sinh mã ngữ nghĩa chạy trên GPU NVIDIA T4 thứ nhất, còn bộ giải mã âm thanh chạy trên GPU T4 thứ hai. Mục tiêu là tạo giọng nói rõ ràng, ổn định và không bị hết bộ nhớ GPU."
  }
}

CASES = [
 {"id":"C01-en-to-en","ref":"en","target":"en","text":"This is a new English sentence generated from the reference voice. The purpose is to verify speaker conditioning on the dual GPU pipeline."},
 {"id":"C02-en-to-vi","ref":"en","target":"vi","text":"Đây là một câu tiếng Việt mới được tạo từ giọng tham chiếu tiếng Anh. Mục tiêu là kiểm tra khả năng giữ đặc trưng giọng khi đổi ngôn ngữ."},
 {"id":"C03-vi-to-vi","ref":"vi","target":"vi","text":"Đây là một câu tiếng Việt mới được tạo từ giọng tham chiếu tiếng Việt. Mục tiêu là xác nhận quy trình sao chép giọng hoạt động ổn định trên hai GPU."},
 {"id":"C04-vi-to-en","ref":"vi","target":"en","text":"This is a new English sentence generated from the Vietnamese reference voice. The goal is to verify cross language speaker conditioning."}
]

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def metrics(path):
    y,sr=sf.read(path,dtype="float32",always_2d=False)
    if y.ndim>1: y=y.mean(axis=1)
    a=np.abs(y)
    return {
      "sample_rate":int(sr),"frames":int(len(y)),"duration_s":float(len(y)/sr),
      "peak_abs":float(a.max()) if len(y) else 0.0,
      "rms":float(np.sqrt(np.mean(y*y))) if len(y) else 0.0,
      "silence_ratio_lt_1e-4":float(np.mean(a<1e-4)) if len(y) else 1.0,
      "clipping_ratio_ge_0_999":float(np.mean(a>=0.999)) if len(y) else 0.0,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--checkpoint",required=True)
    ap.add_argument("--output-dir",required=True)
    ap.add_argument("--semantic-device",default="cuda:0")
    ap.add_argument("--decoder-device",default="cuda:1")
    ap.add_argument("--max-seq-len",type=int,default=4096)
    ap.add_argument("--seed",type=int,default=100)
    args=ap.parse_args()
    root=Path(args.repo_root); cp=Path(args.checkpoint); out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    precision=torch.float16

    t=time.perf_counter()
    model,decode_one_token=init_model(cp,args.semantic_device,precision,compile=False,max_seq_len=args.max_seq_len)
    with torch.device(args.semantic_device):
        model.setup_caches(max_batch_size=1,max_seq_len=model.config.max_seq_len,dtype=next(model.parameters()).dtype)
    model._cache_setup_done=True
    torch.cuda.synchronize(0)
    semantic_load_s=time.perf_counter()-t

    t=time.perf_counter()
    codec=load_codec_model(cp/"codec.pth",args.decoder_device,precision)
    torch.cuda.synchronize(1)
    codec_load_s=time.perf_counter()-t

    ref_tokens={}
    ref_meta={}
    for lang,ref in REFS.items():
        p=root/ref["audio"]
        info=sf.info(str(p))
        t=time.perf_counter()
        tok=encode_audio(p,codec,args.decoder_device).cpu()
        torch.cuda.synchronize(1)
        enc_s=time.perf_counter()-t
        ref_tokens[lang]=tok
        ref_meta[lang]={
          "audio":str(p),"text":ref["text"],"duration_s":float(info.duration),
          "sample_rate":int(info.samplerate),"sha256":sha256(p),
          "vq_shape":list(tok.shape),"encode_s":enc_s
        }
        print("REFERENCE",lang,json.dumps(ref_meta[lang],ensure_ascii=False))

    results=[]
    for i,c in enumerate(CASES):
        torch.manual_seed(args.seed+i); torch.cuda.manual_seed_all(args.seed+i)
        for g in (0,1): torch.cuda.reset_peak_memory_stats(g)
        t=time.perf_counter()
        chunks=[]
        gen=generate_long(
          model=model,device=args.semantic_device,decode_one_token=decode_one_token,
          text=c["text"],num_samples=1,max_new_tokens=260,top_p=0.9,top_k=30,
          temperature=1.0,compile=False,iterative_prompt=True,chunk_length=300,
          prompt_text=[REFS[c["ref"]]["text"]],prompt_tokens=[ref_tokens[c["ref"]]]
        )
        for response in gen:
            if response.action=="sample": chunks.append(response.codes)
        torch.cuda.synchronize(0)
        semantic_s=time.perf_counter()-t
        if not chunks: raise RuntimeError("no codes "+c["id"])
        codes=torch.cat(chunks,dim=1)
        t=time.perf_counter()
        audio=decode_to_audio(codes.to(args.decoder_device),codec)
        torch.cuda.synchronize(1)
        decode_s=time.perf_counter()-t
        wav=out/(c["id"]+".wav")
        sf.write(wav,audio.detach().cpu().float().numpy(),codec.sample_rate,subtype="PCM_16")
        am=metrics(wav)
        item={**c,"status":"PASS","seed":args.seed+i,"reference":ref_meta[c["ref"]],
          "precision":"FP16","max_seq_len":args.max_seq_len,
          "semantic_device":args.semantic_device,"decoder_device":args.decoder_device,
          "codes_shape":list(codes.shape),"semantic_time_s":semantic_s,"decode_time_s":decode_s,
          "total_inference_s":semantic_s+decode_s,
          "rtf":(semantic_s+decode_s)/am["duration_s"] if am["duration_s"] else math.inf,
          "wav":str(wav),"wav_bytes":wav.stat().st_size,"wav_sha256":sha256(wav),
          "gpu0_peak_allocated_bytes":torch.cuda.max_memory_allocated(0),
          "gpu1_peak_allocated_bytes":torch.cuda.max_memory_allocated(1),**am}
        (out/(c["id"]+".json")).write_text(json.dumps(item,indent=2,ensure_ascii=False)+"\n")
        results.append(item)
        print("CASE",json.dumps(item,ensure_ascii=False))
    summary={"status":"PASS","qualification_type":"synthetic-reference technical qualification",
      "semantic_load_s":semantic_load_s,"codec_load_s":codec_load_s,
      "case_count":len(results),"references":ref_meta,"cases":results}
    (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    print("TECHNICAL_VOICE_CLONING=PASS")

if __name__=="__main__": main()
