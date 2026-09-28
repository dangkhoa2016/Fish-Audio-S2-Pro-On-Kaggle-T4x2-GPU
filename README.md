# Fish Audio S2 Pro on Kaggle T4x2 GPU

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

[![Repository Audit](https://github.com/dangkhoa2016/Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/dangkhoa2016/Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Release](https://img.shields.io/badge/release-v1.0.0-blue)
![Hardware](https://img.shields.io/badge/Kaggle-T4%20x2-20BEFF)
![Runtime](https://img.shields.io/badge/Fish%20Speech-pinned-success)

Reproducible Fish Audio S2 Pro inference on Kaggle using two NVIDIA Tesla T4 16 GB GPUs with explicit model-component placement.


## Status

All qualified runtime and release paths are complete. The FP16 dual-GPU baseline passed, single-T4 INT8 qualification proved full INT8-semantic + FP16-codec TTS on a single Tesla T4, dual-instance concurrency qualification proved two independent single-T4 INT8 instances can run concurrently on Kaggle T4x2, and clean-room regression reproduced the accepted paths from a fresh Kaggle T4x2 session.

The project is **release-qualified for v1.0.0**. Fresh clean-room regression, reproducible synthetic multi-speaker voice-cloning acceptance, objective speaker verification, and final release-readiness audit have passed.

## Reviewer guide

For a structured review of the engineering work, start with:

- [Documentation guide](docs/README.md)
- [Engineering overview](docs/engineering-overview.md)
- [Qualification matrix](docs/qualification-matrix.md)
- [Reproducibility guide](docs/reproducibility.md)
- [Evidence index](docs/evidence-index.md)
- [Development history](docs/development-history.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Citation](CITATION.cff)

## Working topology

- `cuda:0`: Dual-AR / text-to-semantic / KV cache
- `cuda:1`: codec / reference encoder / audio decoder
- precision: FP16
- batch size: 1
- `max_seq_len`: 4096
- `torch.compile`: OFF

Two T4s are not treated as pooled 32 GB VRAM. The pipeline is explicitly partitioned across the two devices.

## Model and source

- Original model: `fishaudio/s2-pro`
- Kaggle mirror: `dangkhoa2016/fishaudio-s2-pro`
- Runtime source: official `fishaudio/fish-speech`
- Pinned upstream revision: `214da3cd841bda85da2496b96cd3c4d7edb1337e`

See `references/upstream.lock` and `references/model-source.md`.

## Verified milestones

| Area | Result |
|---|---|
| Kaggle T4x2 CUDA preflight | PASS |
| Single-T4 semantic generation | PASS |
| Single-T4 full FP16 TTS | Expected OOM |
| Single-T4 INT8 semantic + FP16 codec | PASS |
| Two independent single-T4 INT8 instances | PASS |
| Dual-T4 FP16 CLI TTS | PASS |
| English synthesis | PASS |
| Vietnamese synthesis | PASS |
| Technical voice cloning | PASS |
| Local HTTP API | PASS |
| Controlled benchmark | PASS |
| Fresh Kaggle T4x2 clean-room regression | PASS |
| Synthetic multi-speaker voice cloning (8 speakers / 12 clones + 2 repeats) | PASS |
| Independent speaker-embedding top-1 (same / cross language) | 8/8 / 4/4 |

The final reproducible voice-cloning gate uses an independent VoxCPM2 synthetic speaker bank: 8/8 same-language cases and 4/4 cross-language cases identify the intended speaker as top-1 among all eight references using an independent speaker encoder. See `docs/synthetic-multispeaker-voice-cloning-acceptance.md`.

## Controlled benchmark

Baseline: FP16, batch 1, `max_seq_len=4096`, compile OFF, 2 warmups, 8 scenarios, 5 measured runs per scenario.

| Scenario | Median wall | Median audio | Median RTF | Semantic tok/s |
|---|---:|---:|---:|---:|
| EN short | 13.194 s | 4.923 s | 2.720 | 8.276 |
| VI short | 12.869 s | 4.737 s | 2.698 | 8.361 |
| EN medium | 36.011 s | 13.653 s | 2.644 | 8.335 |
| VI medium | 35.111 s | 13.189 s | 2.644 | 8.308 |
| EN long | 58.209 s | 22.245 s | 2.617 | 8.297 |
| VI long | 57.921 s | 22.245 s | 2.604 | 8.338 |
| Clone EN | 12.384 s | 4.505 s | 2.749 | 8.217 |
| Clone VI | 10.361 s | 3.715 s | 2.800 | 8.156 |

Cold model-ready time was about 96.709 s. GPU0 stayed near 10.9 GB allocated; GPU1 was about 4.4–5.5 GB. No OOM or clipping occurred in the 40 measured runs.

Full methodology and results: `docs/benchmark-methodology.md` and `docs/controlled-benchmark-results.md`. Single-T4 INT8 results are in `docs/single-t4-int8.md`. Parallel independent-instance results are in `docs/dual-instance-concurrency.md`.

## Reproduction

The repository contains the scripts and patches used for the qualification flow:

1. `scripts/bootstrap_kaggle.sh`
2. `scripts/preflight.sh`
3. `scripts/setup_runtime.sh`
4. `scripts/inventory_model.py`
5. `scripts/apply_upstream_patch.sh`
6. `scripts/run_dual_gpu_fp16.sh`
7. `scripts/qualify_text_synthesis.py`
8. `scripts/qualify_voice_cloning.py`
9. `scripts/run_api_server_dual_gpu.sh`
10. `scripts/run_controlled_benchmark.py`
11. `scripts/quantize_single_t4_int8.py`
12. `scripts/run_single_t4_int8.sh`
13. `scripts/run_api_server_single_t4_int8.sh`
14. `scripts/setup_voxcpm2_reference_runtime.sh`
15. `scripts/generate_synthetic_speaker_bank.py`
16. `scripts/qualify_synthetic_multispeaker.py`
17. `scripts/score_synthetic_speakers.py`
18. `scripts/check_synthetic_repeatability.py`
19. `scripts/build_synthetic_review_html.py`

For a fresh session, start with `scripts/bootstrap_kaggle.sh`; it checks out the exact upstream commit from `references/upstream.lock` and inventories the attached Kaggle model. Then run preflight, runtime setup, patch application, and the desired qualification runner.

dual-instance concurrency qualification exact two-instance launch commands are documented in `docs/dual-instance-concurrency.md`.

Patch artifacts are under `patches/`. Runtime evidence and retained outputs are under `evidence/` and `results/`.

Synthetic multi-speaker voice-cloning acceptance is documented in `docs/synthetic-multispeaker-voice-cloning-acceptance.md`. The reference source is recorded in `references/synthetic-reference-source.md`, and `reports/synthetic-multispeaker-review.html` provides side-by-side listening.

## Known limitations

- Full FP16 TTS does not fit on one T4 in the tested upstream configuration.
- `max_seq_len=4096` is intentionally lower than the upstream S2 Pro setting of 32768.
- WebUI has not been built or qualified.
- No public tunnel test is included.
- The final release gate is based on reproducible synthetic references; this does not claim universal equivalence to arbitrary real-human voice evaluation.
- INT8 semantic throughput is slower than FP16 and subjective quality equivalence has not been claimed.
- `torch.compile` is not part of the baseline.

## Licensing

Model weights are not included in this repository. Review `LICENSE-NOTES.md` and the upstream/model licenses before use or redistribution.

## Project contract

See `PROJECT-CONTRACT.md` for the locked baseline and acceptance criteria. Final release audit: `docs/final-release-readiness.md`.
