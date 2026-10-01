# Fish Audio S2 Pro on Kaggle T4x2 GPU

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

[![Repository Audit](https://github.com/dangkhoa2016/Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/dangkhoa2016/Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml)
[![Original repository code: MIT](https://img.shields.io/badge/original%20repository%20code-MIT-yellow.svg)](LICENSE)
[![Fish Audio materials: Research License](https://img.shields.io/badge/Fish%20Audio%20materials-Research%20License-orange.svg)](THIRD_PARTY_LICENSES/FISH-AUDIO-RESEARCH-LICENSE)
![Release](https://img.shields.io/badge/release-v1.0.0-blue)
![Hardware](https://img.shields.io/badge/Kaggle-T4%20x2-20BEFF)
![Runtime](https://img.shields.io/badge/Fish%20Speech-pinned-success)

**Built with Fish Audio.**

Reproducible S2 Pro inference on Kaggle using two NVIDIA Tesla T4 16 GB GPUs with explicit model-component placement.

This repository is an engineering qualification project rather than a one-off notebook. It combines runtime implementation, clean-room reproducibility, retained evidence, controlled benchmarking, independent speaker verification, repository governance, and release documentation so that technical claims can be reviewed against concrete artifacts.

## Status

All qualified runtime and release paths are complete. The FP16 dual-GPU baseline passed, single-T4 INT8 qualification proved full INT8-semantic + FP16-codec TTS on a single Tesla T4, dual-instance concurrency qualification proved two independent single-T4 INT8 instances can run concurrently on Kaggle T4x2, and clean-room regression reproduced the accepted paths from a fresh Kaggle T4x2 session.

The project is **release-qualified for v1.0.0**. Fresh clean-room regression, reproducible synthetic multi-speaker voice-cloning acceptance, objective speaker verification, and final release-readiness audit have passed.

### Key capabilities

- Dual-T4 FP16 inference with explicit component placement.
- English text synthesis plus technically qualified Vietnamese synthesis across short, medium, long, and expressive cases; native Vietnamese pronunciation is not qualified.
- Same-language and cross-language voice cloning.
- Local HTTP API qualification.
- Controlled FP16 benchmark with retained machine-readable results.
- Single-T4 INT8 semantic inference with FP16 codec.
- Two independent INT8 instances across T4x2 for concurrency scaling.
- Fresh-session clean-room regression.
- Independent VoxCPM2 synthetic reference bank and WavLM speaker verification.
- Deterministic repeatability checks and side-by-side listening report.

## Documents

The root README is the project overview. For engineering review, reproduction, and claim-to-evidence tracing, use the documentation set below.

### Start here

- [Documentation guide](docs/README.md) — navigation for reviewers and operators.
- [Engineering overview](docs/engineering-overview.md) — system boundaries, hardware topology, operating modes, and release scope.
- [Qualification matrix](docs/qualification-matrix.md) — tested capability, hardware, configuration, result, and authority artifact.
- [Reproducibility guide](docs/reproducibility.md) — fresh-session procedure and acceptance rules.
- [Evidence index](docs/evidence-index.md) — map from claims to logs, JSON summaries, WAV outputs, and reports.
- [Development history](docs/development-history.md) — chronological engineering narrative and corrective discoveries.

### Architecture and methodology

- [Architecture](docs/architecture.md)
- [Benchmark methodology](docs/benchmark-methodology.md)
- [Troubleshooting](docs/troubleshooting.md)

### Qualification records

- [bilingual text-synthesis qualification — EN/VI text-only qualification](docs/bilingual-text-synthesis.md)
- [technical voice-cloning qualification — synthetic-reference voice cloning](docs/technical-voice-cloning.md)
- [local API qualification — local API qualification](docs/local-api-qualification.md)
- [controlled benchmark — controlled benchmark](docs/controlled-benchmark-results.md)
- [single-T4 INT8 qualification — single-T4 INT8](docs/single-t4-int8.md)
- [dual-instance concurrency qualification — two independent INT8 instances](docs/dual-instance-concurrency.md)
- [release/productization audit — release/productization audit](docs/release-productization-audit.md)
- [clean-room regression — fresh clean-room regression](docs/cleanroom-regression.md)
- [Synthetic multi-speaker voice-cloning acceptance](docs/synthetic-multispeaker-voice-cloning-acceptance.md)
- [Final release readiness](docs/final-release-readiness.md)

### Repository governance

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Citation metadata](CITATION.cff)
- [Project contract](PROJECT-CONTRACT.md)

## Working topology

- `cuda:0`: Dual-AR / text-to-semantic / KV cache
- `cuda:1`: codec / reference encoder / audio decoder
- precision: FP16
- batch size: 1
- `max_seq_len`: 4096
- `torch.compile`: OFF

Two T4s are not treated as pooled 32 GB VRAM. The pipeline is explicitly partitioned across the two devices.

### Qualified operating modes

**Dual-T4 FP16** is the primary quality/performance baseline for bilingual synthesis, cloning, local API serving, and benchmarking.

**Single-T4 INT8 semantic + FP16 codec** is a capacity-oriented fallback. It fits complete TTS on one Tesla T4, but the measured semantic path is slower than FP16 and is not presented as a speed optimization.

**Two independent single-T4 INT8 instances** use one isolated process per GPU. The clean-room concurrency rerun reproduced approximately `2.0126x` aggregate scaling for the tested deterministic request. This is process-level parallelism, not pooled model memory.

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

### Independent voice-cloning verification

The final gate deliberately avoids circular self-reference: S2 Pro does not generate the reference bank used to evaluate S2 Pro.

1. VoxCPM2 generates eight synthetic reference speakers: four English and four Vietnamese.
2. S2 Pro produces eight same-language and four cross-language clone cases.
3. An independent WavLM-based speaker encoder compares every clone against all eight references.
4. The intended reference speaker ranks top-1 in `12/12` cases.
5. Two deterministic repeats are regenerated and verified byte-for-byte.

Measured verification summary:

```text
top-1 intended speaker    12 / 12
mean intended cosine      ~0.96917
mean impostor margin      ~0.14344
repeatability             2 / 2 byte-identical
```

This demonstrates reproducible speaker-conditioning behavior on the tested synthetic bank; it does not claim universal equivalence for arbitrary real-human voices.

### Vietnamese pronunciation boundary

The Vietnamese pipeline is technically functional: reference-free generation, same-language VoxCPM2 reference conditioning, cross-language conditioning, and local API requests all execute successfully on the qualified T4x2 runtime. Human listening on 2026-10-01 nevertheless found that Vietnamese remained noticeably non-native, with only modest improvement from same-language VoxCPM2 conditioning.

v1.0.0 therefore claims **Vietnamese pipeline compatibility**, not native Vietnamese pronunciation or tonal naturalness:

```text
VIETNAMESE_PIPELINE_COMPATIBILITY=PASS
VIETNAMESE_NATIVE_PRONUNCIATION=NOT_QUALIFIED
```

No corresponding CUDA, memory, API, or split-device execution failure was observed. In this release the behavior is treated as a tested model-capability limitation rather than a Kaggle T4x2 integration defect.

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

Reproduction is documented separately so the root README stays focused on project scope, validated results, and operating modes.

See the **[Reproducibility Guide](docs/reproducibility.md)** for the required Kaggle environment, clean-session contract, exact bootstrap sequence, the purpose of every reproduction/qualification script, expected inputs and outputs, operating-mode workflows, evidence locations, and acceptance rules.

For an interactive Kaggle entry point, use **[`notebooks/kaggle-production-demo.ipynb`](notebooks/kaggle-production-demo.ipynb)** with **GPU T4 x2** and the attached `dangkhoa2016/fishaudio-s2-pro` model. The notebook preserves the six-case EN/VI run as a technical baseline and uses the independent VoxCPM2 speaker bank for conditioning evidence. Its final scorecard explicitly separates technical Vietnamese compatibility from native-pronunciation quality; `PASS` markers must not be interpreted as native Vietnamese accent validation.

## Repository audit

Run the same lightweight repository audit mirrored by GitHub Actions with:

```bash
make audit
```

The audit covers shell syntax, Python compilation, JSON validity, whitespace, accidental tracked model weights, and common secret-pattern checks.

## Known limitations

- Full FP16 TTS does not fit on one T4 in the tested upstream configuration.
- `max_seq_len=4096` is intentionally lower than the upstream S2 Pro setting of 32768.
- WebUI has not been built or qualified.
- No public tunnel test is included.
- The final release gate is based on reproducible synthetic references; this does not claim universal equivalence to arbitrary real-human voice evaluation.
- Vietnamese generation and conditioning are technically functional, but native Vietnamese pronunciation / tonal naturalness is **NOT QUALIFIED**.
- INT8 semantic throughput is slower than FP16 and subjective quality equivalence has not been claimed.
- `torch.compile` is not part of the baseline.

## Licensing

Original code and documentation authored specifically for this repository are licensed under the [MIT License](LICENSE), except where a file is derived from or modifies Fish Audio materials:

```text
Copyright (c) 2026 Đăng Khoa <i.am@dangkhoa.dev>
```

Fish Audio S2 Pro model weights, upstream Fish Speech code, and repository patch artifacts that modify Fish Speech remain governed by the **Fish Audio Research License** and are **not** relicensed under MIT.

The patch scope and licensing boundary are documented in [patches/README.md](patches/README.md). See also [LICENSE-NOTES.md](LICENSE-NOTES.md), [NOTICE.txt](NOTICE.txt), and the [retained Fish Audio Research License](THIRD_PARTY_LICENSES/FISH-AUDIO-RESEARCH-LICENSE). Model weights are not included in this repository.

Commercial use of Fish Audio materials or derivative works requires a separate written license from Fish Audio under the retained license terms.

## Release boundary

The stable release is **v1.0.0**. It represents the documented Kaggle T4x2 configurations, retained evidence, reproducibility checks, and repository governance described above.

See [PROJECT-CONTRACT.md](PROJECT-CONTRACT.md) for the locked baseline and acceptance criteria, and [final release readiness](docs/final-release-readiness.md) for the release audit.
