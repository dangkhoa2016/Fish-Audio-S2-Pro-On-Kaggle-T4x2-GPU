# Chỉ mục evidence

> 🌐 Language / Ngôn ngữ: [English](evidence-index.md) | **Tiếng Việt**

Tài liệu này ánh xạ public claims tới retained evidence để reviewer có thể xác minh từng statement mà không cần đọc toàn bộ development history.

## Environment và baseline

- GPU preflight: `evidence/gpu-preflight.txt`, `evidence/environment-preflight.txt`, `evidence/system-inventory.txt`, `results/gpu-preflight.json`
- Runtime environment: `evidence/runtime-environment.txt`, `evidence/runtime-pip-freeze.txt`
- Dual-GPU model load: `evidence/dual-t4-fp16.log`, `results/dual-t4-fp16-result.json`

## FP16 qualification

- EN/VI text-only: `evidence/bilingual-text-synthesis.log.gz`
- Voice cloning: `evidence/technical-voice-cloning.log.gz`
- Local API: `evidence/local-api-server.log`
- Controlled benchmark: `evidence/controlled-benchmark.log.gz` và artifacts trong `results/controlled-benchmark/`

## INT8 qualification

- Conversion: `evidence/single-t4-int8-convert.log`
- EN/VI full TTS: `evidence/single-t4-int8-en.log`, `evidence/single-t4-int8-vi.log`
- Machine-readable summary: `results/single-t4-int8/summary.json`
- Parallel instances: `results/dual-instance-concurrency/summary.json`

## Clean-room regression

- Summary: `results/cleanroom-regression/summary.json`
- Logs và retained WAV outputs: `evidence/cleanroom-regression/`, `results/cleanroom-regression/`

## Kaggle production notebook

- Fresh-session Run All record: `evidence/kaggle-production-demo.log`
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

Logs mô tả execution, JSON giữ structured measurements, WAV giữ representative audio outputs và Markdown giải thích scope/interpretation. Không lớp nào được dùng để silently mở rộng claim vượt quá configuration đã kiểm tra.
