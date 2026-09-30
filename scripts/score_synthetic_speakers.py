#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import torch
import torchaudio
from transformers import AutoFeatureExtractor, WavLMForXVector

def embed(path, extractor, model, device):
    wav,sr=torchaudio.load(str(path))
    wav=wav.mean(dim=0)
    if sr!=16000:
        wav=torchaudio.functional.resample(wav,sr,16000)
    x=extractor(wav.numpy(),sampling_rate=16000,return_tensors="pt",padding=True)
    vals=x["input_values"].to(device)
    with torch.inference_mode():
        emb=model(vals).embeddings[0]
        emb=torch.nn.functional.normalize(emb,dim=0)
    return emb.cpu()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--model-id",default="microsoft/wavlm-base-plus-sv")
    ap.add_argument("--revision",default="feb593a6c23c1cc3d9510425c29b0a14d2b07b1e")
    ap.add_argument("--output",default="results/synthetic-multispeaker-acceptance/speaker-verification.json")
    ap.add_argument("--device",default="cuda:0")
    args=ap.parse_args()
    root=Path(args.repo_root).resolve()
    bank=json.loads((root/"results/synthetic-speaker-bank/summary.json").read_text())
    qual=json.loads((root/"results/synthetic-multispeaker-acceptance/summary.json").read_text())
    device=torch.device(args.device if torch.cuda.is_available() else "cpu")
    extractor=AutoFeatureExtractor.from_pretrained(args.model_id,revision=args.revision)
    model=WavLMForXVector.from_pretrained(args.model_id,revision=args.revision,use_safetensors=False).to(device).eval()
    refs={}
    for sp in bank["speakers"]:
        p=root/"results/synthetic-speaker-bank"/sp["wav"]
        refs[sp["id"]]=embed(p,extractor,model,device)
        print("REFERENCE_EMBED",sp["id"],flush=True)
    cases=[]
    for c in qual["cases"]:
        op=root/c["output"]["path"]
        e=embed(op,extractor,model,device)
        scores={sid:float(torch.dot(e,re).item()) for sid,re in refs.items()}
        ranked=sorted(scores.items(),key=lambda kv:kv[1],reverse=True)
        correct=c["speaker_id"]
        rank=next(i+1 for i,(sid,_) in enumerate(ranked) if sid==correct)
        correct_score=scores[correct]
        best_impostor=max(v for sid,v in scores.items() if sid!=correct)
        item={
          "case_id":c["id"],"mode":c["mode"],"source_lang":c["source_lang"],
          "target_lang":c["target_lang"],"expected_speaker":correct,
          "rank":rank,"top1_speaker":ranked[0][0],"top1_score":ranked[0][1],
          "correct_score":correct_score,"best_impostor_score":best_impostor,
          "margin_vs_best_impostor":correct_score-best_impostor,
          "scores":scores
        }
        cases.append(item)
        print("CASE",c["id"],"rank",rank,"correct",round(correct_score,5),
              "margin",round(item["margin_vs_best_impostor"],5),flush=True)
    top1=sum(x["rank"]==1 for x in cases)
    same=[x for x in cases if x["mode"]=="same"]
    cross=[x for x in cases if x["mode"]=="cross"]
    summary={
      "verifier":args.model_id,"verifier_revision":args.revision,"method":"cosine similarity of normalized WavLM x-vector embeddings",
      "reference_count":len(refs),"case_count":len(cases),
      "top1_count":top1,"top1_accuracy":top1/len(cases),
      "same_language_top1_count":sum(x["rank"]==1 for x in same),
      "same_language_count":len(same),
      "cross_language_top1_count":sum(x["rank"]==1 for x in cross),
      "cross_language_count":len(cross),
      "mean_correct_score":float(np.mean([x["correct_score"] for x in cases])),
      "mean_margin_vs_best_impostor":float(np.mean([x["margin_vs_best_impostor"] for x in cases])),
      "min_margin_vs_best_impostor":float(np.min([x["margin_vs_best_impostor"] for x in cases])),
      "cases":cases
    }
    out=root/args.output; out.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    print("SPEAKER_TOP1",top1,"/",len(cases),flush=True)
    print("SAME_TOP1",summary["same_language_top1_count"],"/",len(same),flush=True)
    print("CROSS_TOP1",summary["cross_language_top1_count"],"/",len(cross),flush=True)

if __name__=="__main__": main()
