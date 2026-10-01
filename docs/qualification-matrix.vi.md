# Ma trận qualification

> 🌐 Language / Ngôn ngữ: [English](qualification-matrix.md) | **Tiếng Việt**

| Capability | Hardware | Configuration | Result | Authority |
|---|---|---|---|---|
| CUDA / dual-T4 preflight | Kaggle T4x2 | 2 × Tesla T4 | PASS | `results/gpu-preflight.json` |
| Single-T4 semantic generation | 1 × T4 | FP16 semantic | PASS | `evidence/single-t4-fp16-semantic.log` |
| Single-T4 full FP16 TTS | 1 × T4 | FP16 semantic + codec | Expected OOM | `evidence/single-t4-fp16-full.log` |
| Dual-T4 model load | T4x2 | split FP16 | PASS | `results/dual-t4-fp16-result.json` |
| EN text-only TTS | T4x2 | split FP16 | PASS | `docs/bilingual-text-synthesis.md` |
| VI text-only TTS | T4x2 | split FP16; technical generation | PASS (technical) | `docs/bilingual-text-synthesis.md` |
| VI native pronunciation / tonal naturalness | T4x2 | human listening: reference-free + same-language VoxCPM2-conditioned | NOT QUALIFIED | `docs/final-release-readiness.vi.md` |
| Voice cloning | T4x2 | split FP16 | PASS | `docs/technical-voice-cloning.md` |
| Local HTTP API | T4x2 | split FP16 | PASS | `docs/local-api-qualification.md` |
| Controlled benchmark | T4x2 | split FP16 | PASS | `docs/controlled-benchmark-results.md` |
| Single-T4 full TTS | 1 × T4 | INT8 semantic + FP16 codec | PASS | `results/single-t4-int8/summary.json` |
| Parallel API capacity | T4x2 | 2 isolated INT8 instances | PASS | `results/dual-instance-concurrency/summary.json` |
| Fresh clean-room regression | Kaggle T4x2 | release baseline | PASS | `results/cleanroom-regression/summary.json` |
| Kaggle production notebook | fresh Kaggle T4x2 | bilingual FP16 + voice cloning + local API | PASS (technical) | `results/notebook-production-demo/production-demo-summary.json` |
| Synthetic speaker bank | 1 × T4 | VoxCPM2 Voice Design | 8/8 PASS | `results/synthetic-speaker-bank/summary.json` |
| Multi-speaker cloning | T4x2 | 8 same + 4 cross-language | 12/12 PASS | `results/synthetic-multispeaker-acceptance/summary.json` |
| Speaker identification | CPU/GPU verifier | pinned WavLM x-vector | 12/12 top-1 | `results/synthetic-multispeaker-acceptance/speaker-verification.json` |
| Deterministic repeats | T4x2 | fixed inputs + seeds | 2/2 byte-identical | `results/synthetic-multispeaker-repeatability/summary.json` |

## Diễn giải

PASS nghĩa là **technical acceptance condition** tương ứng đã được quan sát dưới configuration được ghi và authority artifact đã được retained. Đây không phải claim cho native accent, pronunciation, tonal naturalness hoặc subjective language quality chưa được qualification. Native Vietnamese pronunciation được theo dõi riêng là NOT QUALIFIED.

## Release-critical gates

Release yêu cầu dual-T4 baseline, fresh-session regression, repository audit và reproducible multi-speaker gate PASS. Optional experiment không được tự động biến thành release requirement.
