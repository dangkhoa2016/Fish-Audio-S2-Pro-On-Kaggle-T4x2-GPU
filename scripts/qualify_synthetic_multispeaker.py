#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, time
from pathlib import Path
import numpy as np
import soundfile as sf
import torch
from fish_speech.models.text2semantic.inference import (
    decode_to_audio, encode_audio, generate_long, init_model, load_codec_model
)

TARGETS = {
 "en_same":"The cloned speaker is now reading a completely new English sentence. This sample tests whether vocal identity remains stable when the words and rhythm differ from the reference recording.",
 "vi_same":"Giọng được sao chép đang đọc một câu tiếng Việt hoàn toàn mới. Mẫu này kiểm tra xem đặc trưng người nói có được giữ ổn định khi nội dung và nhịp điệu khác với bản tham chiếu hay không.",
 "en_cross":"The same synthetic speaker is now speaking English in a cross language cloning test. The sentence is intentionally different from every reference passage.",
 "vi_cross":"Cùng một giọng tổng hợp đang nói tiếng Việt trong bài kiểm thử sao chép xuyên ngôn ngữ. Nội dung câu này hoàn toàn khác với đoạn tham chiếu ban đầu."
}
CROSS_IDS={"en-f01","en-m02","vi-f01","vi-m02"}

def sha256(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()

def metrics(p):
 y,sr=sf.read(p,dtype="float32",always_2d=False)
 if y.ndim>1:y=y.mean(axis=1)
 a=np.abs(y)
 return {"sample_rate":int(sr),"frames":int(len(y)),"duration_s":float(len(y)/sr),
  "peak_abs":float(a.max()) if len(y) else 0.0,
  "rms":float(np.sqrt(np.mean(y*y))) if len(y) else 0.0,
  "silence_ratio_lt_1e_4":float(np.mean(a<1e-4)) if len(y) else 1.0,
  "clipping_ratio_ge_0_999":float(np.mean(a>=0.999)) if len(y) else 0.0}

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--repo-root",required=True); ap.add_argument("--checkpoint",required=True)
 ap.add_argument("--speaker-bank",default="results/synthetic-speaker-bank/summary.json")
 ap.add_argument("--output-dir",default="results/synthetic-multispeaker-acceptance")
 ap.add_argument("--semantic-device",default="cuda:0"); ap.add_argument("--decoder-device",default="cuda:1")
 ap.add_argument("--max-seq-len",type=int,default=4096); ap.add_argument("--seed",type=int,default=20260930)
 args=ap.parse_args()
 root=Path(args.repo_root).resolve(); cp=Path(args.checkpoint).resolve()
 bank=json.loads((root/args.speaker_bank).read_text())
 if bank.get("status")!="PASS" or bank.get("speaker_count")!=8: raise ValueError("speaker bank must be PASS with 8 speakers")
 out=(root/args.output_dir).resolve(); out.mkdir(parents=True,exist_ok=True)
 precision=torch.float16
 t=time.perf_counter(); model,decode_one_token=init_model(cp,args.semantic_device,precision,compile=False,max_seq_len=args.max_seq_len)
 with torch.device(args.semantic_device):
  model.setup_caches(max_batch_size=1,max_seq_len=model.config.max_seq_len,dtype=next(model.parameters()).dtype)
 model._cache_setup_done=True; torch.cuda.synchronize(0); semantic_load_s=time.perf_counter()-t
 t=time.perf_counter(); codec=load_codec_model(cp/"codec.pth",args.decoder_device,precision)
 torch.cuda.synchronize(1); codec_load_s=time.perf_counter()-t
 refs={}
 for sp in bank["speakers"]:
  p=(root/"results/synthetic-speaker-bank"/sp["wav"]).resolve()
  t=time.perf_counter(); tok=encode_audio(p,codec,args.decoder_device).cpu()
  torch.cuda.synchronize(1)
  refs[sp["id"]]={"speaker":sp,"path":p,"tokens":tok,"encode_s":time.perf_counter()-t}
  print("REFERENCE",sp["id"],list(tok.shape),flush=True)
 cases=[]
 for sp in bank["speakers"]:
  cases.append({"id":sp["id"]+"-same","speaker_id":sp["id"],"source_lang":sp["language"],"target_lang":sp["language"],"mode":"same"})
  if sp["id"] in CROSS_IDS:
   target="vi" if sp["language"]=="en" else "en"
   cases.append({"id":sp["id"]+"-cross-"+target,"speaker_id":sp["id"],"source_lang":sp["language"],"target_lang":target,"mode":"cross"})
 results=[]
 for idx,c in enumerate(cases):
  ref=refs[c["speaker_id"]]; sp=ref["speaker"]
  key=(c["target_lang"]+"_same") if c["mode"]=="same" else (c["target_lang"]+"_cross")
  text=TARGETS[key]
  seed=args.seed+idx; torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
  for g in (0,1): torch.cuda.reset_peak_memory_stats(g)
  t=time.perf_counter(); chunks=[]
  gen=generate_long(model=model,device=args.semantic_device,decode_one_token=decode_one_token,
    text=text,num_samples=1,max_new_tokens=280,top_p=0.9,top_k=30,temperature=1.0,
    compile=False,iterative_prompt=True,chunk_length=300,
    prompt_text=[sp["transcript"]],prompt_tokens=[ref["tokens"]])
  for response in gen:
   if response.action=="sample": chunks.append(response.codes)
  torch.cuda.synchronize(0); semantic_s=time.perf_counter()-t
  if not chunks: raise RuntimeError("no codes "+c["id"])
  codes=torch.cat(chunks,dim=1)
  t=time.perf_counter(); audio=decode_to_audio(codes.to(args.decoder_device),codec)
  torch.cuda.synchronize(1); decode_s=time.perf_counter()-t
  wav=out/(c["id"]+".wav"); sf.write(wav,audio.detach().cpu().float().numpy(),codec.sample_rate,subtype="PCM_16")
  m=metrics(wav); technical=(m["duration_s"]>0.5 and m["rms"]>1e-5 and m["clipping_ratio_ge_0_999"]==0.0)
  item={**c,"status":"PASS" if technical else "FAIL","seed":seed,"target_text":text,
    "reference":{"path":str(ref["path"].relative_to(root)),"sha256":sp["wav_sha256"],"transcript":sp["transcript"],
      "duration_s":sp["duration_s"],"generator":sp["generator"],"description":sp["description"],"vq_shape":list(ref["tokens"].shape)},
    "output":{"path":str(wav.relative_to(root)),"bytes":wav.stat().st_size,"sha256":sha256(wav),**m},
    "timing":{"reference_encode_s":ref["encode_s"],"semantic_s":semantic_s,"decode_s":decode_s,
      "total_s":semantic_s+decode_s,"rtf":(semantic_s+decode_s)/m["duration_s"]},
    "peak_allocated_bytes":{"gpu0":torch.cuda.max_memory_allocated(0),"gpu1":torch.cuda.max_memory_allocated(1)}}
  (out/(c["id"]+".json")).write_text(json.dumps(item,indent=2,ensure_ascii=False)+"\n")
  results.append(item); print("CASE",json.dumps(item,ensure_ascii=False),flush=True)
 passed=sum(x["status"]=="PASS" for x in results)
 summary={"status":"PASS" if passed==len(results) else "FAIL",
  "qualification_type":"independent synthetic multi-speaker voice-cloning acceptance",
  "reference_generator":"VoxCPM2","speaker_count":8,"case_count":len(results),"passed":passed,
  "same_language_cases":sum(x["mode"]=="same" for x in results),"cross_language_cases":sum(x["mode"]=="cross" for x in results),
  "semantic_load_s":semantic_load_s,"codec_load_s":codec_load_s,"cases":results,
  "speaker_similarity_status":"PENDING_OBJECTIVE_SCORING_AND_HUMAN_SPOT_CHECK"}
 (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
 print("SYNTHETIC_MULTISPEAKER_TECHNICAL="+summary["status"],flush=True)
 if summary["status"]!="PASS": raise SystemExit(2)

if __name__=="__main__": main()
