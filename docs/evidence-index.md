# Evidence Index

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](evidence-index.vi.md)

This document maps public claims to retained evidence. It is intended for reviewers who want to verify a statement without reading the entire development history.

## Environment and baseline

- GPU preflight: `evidence/gpu-preflight.txt, `evidence/environment-preflight.txt`, `evidence/system-inventory.txt``, `results/gpu-preflight.json`
- Runtime environment: `evidence/runtime-environment.txt`, `evidence/runtime-pip-freeze.txt`
- Dual-GPU model load: `evidence/dual-t4-fp16.log`, `results/dual-t4-fp16-result.json`

## FP16 qualification

- EN/VI text-only: `evidence/bilingual-text-synthesis.log.gz`
- Voice cloning: `evidence/technical-voice-cloning.log.gz`
- Local API: `evidence/local-api-server.log`
- Controlled benchmark: `evidence/controlled-benchmark.log.gz` and controlled-benchmark result artifacts

## INT8 qualification

- Conversion: `evidence/single-t4-int8-convert.log`
- EN/VI full TTS: `evidence/single-t4-int8-en-full.log`, `evidence/single-t4-int8-vi-full.log`
- Machine-readable summary: `results/single-t4-int8/summary.json`
- Parallel instances: `results/dual-instance-concurrency/summary.json`

## Clean-room regression

- Summary: `results/cleanroom-regression/summary.json`
- Logs and retained WAV outputs: `evidence/cleanroom-regression/`, `results/cleanroom-regression/`

## Kaggle production notebook

- Clean fresh-session Run All record: `evidence/kaggle-production-demo.log`
- Machine-readable scorecard: `results/notebook-production-demo/production-demo-summary.json`
- Local API outputs: `results/notebook-production-demo/api-en.wav`, `results/notebook-production-demo/api-vi.wav`
- Canonical notebook: `notebooks/kaggle-production-demo.ipynb`

## Synthetic multi-speaker acceptance

- VoxCPM2 reference bank: `results/synthetic-speaker-bank/summary.json`
- S2 Pro clone matrix: `results/synthetic-multispeaker-acceptance/summary.json`
- Independent WavLM verification: `results/synthetic-multispeaker-acceptance/speaker-verification.json`
- Repeatability: `results/synthetic-multispeaker-repeatability/summary.json`
- Listening report: `reports/synthetic-multispeaker-review.html`

## Release authority

- Project contract: `PROJECT-CONTRACT.md`
- Productization audit: `docs/release-productization-audit.md`
- Final release audit: `docs/final-release-readiness.md`
- Release notes: `RELEASE_NOTES_v1.0.0.md`

## Evidence policy

Logs document execution, JSON files carry structured measurements, WAV files retain representative audio outputs, and Markdown documents explain scope and interpretation. None of these layers should be used to silently expand a claim beyond the tested configuration.
