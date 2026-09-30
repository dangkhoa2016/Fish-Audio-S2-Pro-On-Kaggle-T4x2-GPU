#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np
import soundfile as sf

SPEAKERS = [
 {"id":"en-f01","language":"en","description":"A young adult woman with a bright, warm, friendly voice, clear articulation, natural conversational pace",
  "transcript":"Today I am recording a clean synthetic reference for a reproducible speech cloning benchmark. I speak at a comfortable pace with clear pronunciation and a relaxed, friendly tone so that the reference contains enough natural vocal detail."},
 {"id":"en-f02","language":"en","description":"A mature woman with a low, calm, slightly husky voice, measured pace, confident documentary style",
  "transcript":"This reference sample is designed to represent a calm and mature speaking style. The recording uses complete sentences, steady pacing, and clear articulation so another speech model can be evaluated against a consistent synthetic speaker identity."},
 {"id":"en-m01","language":"en","description":"A young adult man with an energetic, clear tenor voice, crisp consonants, moderately fast pace",
  "transcript":"This synthetic speaker is reading a controlled English reference passage for repeatable voice cloning tests. The delivery is energetic but natural, with crisp consonants, balanced rhythm, and enough variation to capture a recognizable speaking identity."},
 {"id":"en-m02","language":"en","description":"A middle-aged man with a deep, resonant baritone voice, calm and deliberate pace, professional narration",
  "transcript":"For this benchmark I am providing a stable synthetic reference with a deep and measured speaking style. The passage is long enough to capture timbre, rhythm, and pronunciation while remaining clean, controlled, and easy to reproduce."},
 {"id":"vi-f01","language":"vi","description":"Một phụ nữ trẻ có giọng sáng, ấm áp, thân thiện, phát âm rõ ràng, tốc độ hội thoại tự nhiên",
  "transcript":"Hôm nay tôi đọc một đoạn tham chiếu tổng hợp sạch để kiểm thử khả năng sao chép giọng nói có thể tái lập. Tôi nói với tốc độ tự nhiên, phát âm rõ ràng và giữ giọng thân thiện để mẫu âm thanh có đủ đặc trưng nhận dạng."},
 {"id":"vi-f02","language":"vi","description":"Một phụ nữ trưởng thành có giọng trầm, bình tĩnh, hơi khàn nhẹ, nhịp nói chậm và phong cách thuyết minh tự tin",
  "transcript":"Đây là mẫu giọng tổng hợp được thiết kế với phong cách trưởng thành và điềm tĩnh. Đoạn đọc sử dụng câu đầy đủ, nhịp nói ổn định và phát âm rõ để một mô hình khác có thể kiểm tra khả năng giữ đặc trưng người nói."},
 {"id":"vi-m01","language":"vi","description":"Một nam thanh niên có giọng tenor rõ, năng động, phụ âm sắc nét, tốc độ hơi nhanh nhưng tự nhiên",
  "transcript":"Mẫu giọng tổng hợp này đọc một đoạn tiếng Việt có kiểm soát để phục vụ bài kiểm thử sao chép giọng lặp lại được. Cách nói năng động nhưng tự nhiên, nhịp cân bằng và phát âm rõ giúp tạo ra đặc trưng giọng dễ nhận biết."},
 {"id":"vi-m02","language":"vi","description":"Một người đàn ông trung niên có giọng nam trầm sâu, vang, bình tĩnh, nhịp nói chậm rãi và phong cách dẫn chuyện chuyên nghiệp",
  "transcript":"Trong bài kiểm thử này tôi cung cấp một mẫu tham chiếu tổng hợp ổn định với giọng trầm và nhịp nói chậm rãi. Đoạn đọc đủ dài để thể hiện âm sắc, nhịp điệu và cách phát âm nhưng vẫn sạch và dễ tái tạo."},
]

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def metrics(p: Path) -> dict:
    y,sr=sf.read(p,dtype="float32",always_2d=False)
    if y.ndim>1: y=y.mean(axis=1)
    a=np.abs(y)
    return {
      "sample_rate":int(sr),"channels":1,"frames":int(len(y)),
      "duration_s":float(len(y)/sr),"peak_abs":float(a.max()) if len(y) else 0.0,
      "rms":float(np.sqrt(np.mean(y*y))) if len(y) else 0.0,
      "clipping_ratio_ge_0_999":float(np.mean(a>=0.999)) if len(y) else 0.0,
      "silence_ratio_lt_1e_4":float(np.mean(a<1e-4)) if len(y) else 1.0,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model",required=True)
    ap.add_argument("--output-dir",required=True)
    ap.add_argument("--cfg-value",type=float,default=2.0)
    ap.add_argument("--inference-timesteps",type=int,default=10)
    ap.add_argument("--device",default="cuda")
    args=ap.parse_args()
    from voxcpm import VoxCPM
    out=Path(args.output_dir).resolve(); out.mkdir(parents=True,exist_ok=True)
    t=time.time()
    model=VoxCPM.from_pretrained(args.model,load_denoiser=False,device=args.device)
    load_s=time.time()-t
    rows=[]
    for sp in SPEAKERS:
        text=f"({sp['description']}){sp['transcript']}"
        t=time.time()
        wav=model.generate(text=text,cfg_value=args.cfg_value,inference_timesteps=args.inference_timesteps)
        gen_s=time.time()-t
        path=out/f"{sp['id']}.wav"
        sf.write(path,wav,model.tts_model.sample_rate,subtype="PCM_16")
        m=metrics(path)
        item={**sp,"generator":"VoxCPM2","cfg_value":args.cfg_value,
              "inference_timesteps":args.inference_timesteps,"generation_s":gen_s,
              "wav":path.name,"wav_bytes":path.stat().st_size,"wav_sha256":sha256(path),**m}
        rows.append(item)
        (out/f"{sp['id']}.json").write_text(json.dumps(item,indent=2,ensure_ascii=False)+"\n")
        print("SPEAKER",json.dumps(item,ensure_ascii=False),flush=True)
    valid=[r for r in rows if 10.0<=r["duration_s"]<=30.0 and r["clipping_ratio_ge_0_999"]==0.0 and r["rms"]>1e-5]
    summary={"status":"PASS" if len(valid)==len(rows) else "FAIL",
             "generator":"VoxCPM2","model_path":args.model,"model_load_s":load_s,
             "speaker_count":len(rows),"valid_reference_count":len(valid),"speakers":rows}
    (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    print("SYNTHETIC_SPEAKER_BANK="+summary["status"],flush=True)
    if summary["status"]!="PASS": raise SystemExit(2)

if __name__=="__main__": main()
