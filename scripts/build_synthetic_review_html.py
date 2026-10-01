#!/usr/bin/env python3
from __future__ import annotations
import argparse, html, json
from pathlib import Path

def rel(path: str) -> str:
    return "../" + path.replace("\\","/")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--output",default="reports/synthetic-multispeaker-review.html")
    args=ap.parse_args()
    root=Path(args.repo_root).resolve()
    bank=json.loads((root/"results/synthetic-speaker-bank/summary.json").read_text())
    qual=json.loads((root/"results/synthetic-multispeaker-acceptance/summary.json").read_text())
    ver=json.loads((root/"results/synthetic-multispeaker-acceptance/speaker-verification.json").read_text())
    rep=json.loads((root/"results/synthetic-multispeaker-repeatability/summary.json").read_text())
    cases={c["id"]:c for c in qual["cases"]}
    scores={c["case_id"]:c for c in ver["cases"]}
    repeats={c["case_id"]:c for c in rep["cases"]}
    sections=[]
    for sp in bank["speakers"]:
        sid=sp["id"]; same=cases[sid+"-same"]; sm=scores[sid+"-same"]
        extras=[]
        for c in qual["cases"]:
            if c["speaker_id"]==sid and c["mode"]=="cross":
                sc=scores[c["id"]]
                extras.append(f'''<div><b>Cross-language clone ({html.escape(c["target_lang"].upper())})</b><br>
<audio controls preload="none" src="{html.escape(rel(c["output"]["path"]))}"></audio><br>
WavLM rank {sc["rank"]}/8 · cosine {sc["correct_score"]:.4f} · margin {sc["margin_vs_best_impostor"]:.4f}</div>''')
        if sid+"-same" in repeats:
            rp=repeats[sid+"-same"]
            rp_path=f'results/synthetic-multispeaker-repeatability/{sid}-same-repeat.wav'
            extras.append(f'''<div><b>Deterministic repeat</b><br>
<audio controls preload="none" src="{html.escape(rel(rp_path))}"></audio><br>
Exact SHA-256 match: {str(rp["exact_sha256_match"]).lower()}</div>''')
        ref_path=f'results/synthetic-speaker-bank/{sp["wav"]}'
        sections.append(f'''<section class="card">
<h2>{html.escape(sid)} · {html.escape(sp["language"].upper())}</h2>
<p>{html.escape(sp["description"])}</p>
<div class="grid">
<div><b>VoxCPM2 reference</b><br><audio controls preload="none" src="{html.escape(rel(ref_path))}"></audio><br>{sp["duration_s"]:.2f}s · 48 kHz</div>
<div><b>S2 Pro same-language clone</b><br><audio controls preload="none" src="{html.escape(rel(same["output"]["path"]))}"></audio><br>
WavLM rank {sm["rank"]}/8 · cosine {sm["correct_score"]:.4f} · margin {sm["margin_vs_best_impostor"]:.4f}</div>
{''.join(extras)}
</div>
<p><b>Reference transcript:</b> {html.escape(sp["transcript"])}</p>
<p><b>Clone target:</b> {html.escape(same["target_text"])}</p>
</section>''')
    page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Synthetic Multi-Speaker Voice-Cloning Review</title>
<style>body{{font-family:system-ui,sans-serif;max-width:1200px;margin:auto;padding:24px;line-height:1.5}}
.card{{border:1px solid #ccc;border-radius:12px;padding:18px;margin:18px 0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}
audio{{width:100%;margin-top:8px}}code{{background:#eee;padding:2px 5px;border-radius:4px}}</style></head>
<body><h1>Synthetic Multi-Speaker Voice-Cloning Review</h1>
<p>Reference generator: <b>OpenBMB VoxCPM2</b>. Clone system: <b>Fish Audio S2 Pro</b>. Independent verifier: <b>{html.escape(ver["verifier"])}</b>.</p>
<p>Technical cases: <b>{qual["passed"]}/{qual["case_count"]}</b>. WavLM top-1: <b>{ver["top1_count"]}/{ver["case_count"]}</b>
(same-language {ver["same_language_top1_count"]}/{ver["same_language_count"]}, cross-language {ver["cross_language_top1_count"]}/{ver["cross_language_count"]}).
Deterministic repeat: <b>{sum(x["exact_sha256_match"] for x in rep["cases"])}/{rep["case_count"]}</b>.</p>
<p>Use this page for a quick listening spot-check of speaker identity, pronunciation, naturalness, and obvious artifacts. These are synthetic voices, not recordings of real people.</p>
{''.join(sections)}
</body></html>'''
    out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(page)
    print("REVIEW_HTML",out)
    print("SYNTHETIC_REVIEW_HTML=PASS")

if __name__=="__main__": main()
