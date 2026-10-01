#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, time
from pathlib import Path
import soundfile as sf
import torch
from fish_speech.models.text2semantic.inference import (
    decode_to_audio, encode_audio, generate_long, init_model, load_codec_model
)

CASE_IDS=("en-f01-same","vi-f01-same")

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--checkpoint",required=True)
    ap.add_argument("--output-dir",default="results/synthetic-multispeaker-repeatability")
    ap.add_argument("--semantic-device",default="cuda:0")
    ap.add_argument("--decoder-device",default="cuda:1")
    ap.add_argument("--max-seq-len",type=int,default=4096)
    args=ap.parse_args()
    root=Path(args.repo_root).resolve(); cp=Path(args.checkpoint).resolve()
    summary=json.loads((root/"results/synthetic-multispeaker-acceptance/summary.json").read_text())
    selected=[next(c for c in summary["cases"] if c["id"]==cid) for cid in CASE_IDS]
    out=(root/args.output_dir).resolve(); out.mkdir(parents=True,exist_ok=True)
    precision=torch.float16
    model,decode_one_token=init_model(cp,args.semantic_device,precision,compile=False,max_seq_len=args.max_seq_len)
    with torch.device(args.semantic_device):
        model.setup_caches(max_batch_size=1,max_seq_len=model.config.max_seq_len,dtype=next(model.parameters()).dtype)
    model._cache_setup_done=True
    codec=load_codec_model(cp/"codec.pth",args.decoder_device,precision)
    results=[]
    for c in selected:
        ref_path=root/c["reference"]["path"]
        ref_tokens=encode_audio(ref_path,codec,args.decoder_device).cpu()
        seed=c["seed"]; torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
        chunks=[]
        for response in generate_long(
            model=model,device=args.semantic_device,decode_one_token=decode_one_token,
            text=c["target_text"],num_samples=1,max_new_tokens=280,top_p=0.9,top_k=30,
            temperature=1.0,compile=False,iterative_prompt=True,chunk_length=300,
            prompt_text=[c["reference"]["transcript"]],prompt_tokens=[ref_tokens]):
            if response.action=="sample": chunks.append(response.codes)
        if not chunks: raise RuntimeError("no codes "+c["id"])
        codes=torch.cat(chunks,dim=1)
        audio=decode_to_audio(codes.to(args.decoder_device),codec)
        wav=out/(c["id"]+"-repeat.wav")
        sf.write(wav,audio.detach().cpu().float().numpy(),codec.sample_rate,subtype="PCM_16")
        repeat_hash=sha256(wav); original_hash=c["output"]["sha256"]
        item={"case_id":c["id"],"seed":seed,"original_sha256":original_hash,
              "repeat_sha256":repeat_hash,"exact_sha256_match":repeat_hash==original_hash,
              "original_bytes":c["output"]["bytes"],"repeat_bytes":wav.stat().st_size}
        results.append(item); print("REPEAT",json.dumps(item),flush=True)
    final={"status":"PASS" if all(x["exact_sha256_match"] for x in results) else "NON_BIT_EXACT",
           "case_count":len(results),"cases":results}
    (out/"summary.json").write_text(json.dumps(final,indent=2)+"\n")
    print("SYNTHETIC_REPEATABILITY="+final["status"],flush=True)

if __name__=="__main__": main()
