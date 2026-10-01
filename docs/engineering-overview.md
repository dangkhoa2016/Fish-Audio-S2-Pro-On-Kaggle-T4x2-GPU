# Engineering Overview

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](engineering-overview.vi.md)

## Objective

Run Fish Audio S2 Pro reproducibly on Kaggle's dual Tesla T4 environment while preserving enough evidence for an independent reviewer to distinguish measured behavior from assumptions.

## Hardware model

The project does not treat two 16 GB T4 GPUs as pooled 32 GB memory. The accepted FP16 topology explicitly partitions components:

- GPU0: text-to-semantic / Dual-AR model and KV cache.
- GPU1: codec, reference encoder, and audio decoder.
- Precision: FP16.
- Batch size: 1.
- Maximum sequence length: 4096.
- `torch.compile`: disabled.

This placement is the release baseline.

## Supported operating modes

### Dual-T4 FP16

Primary quality/performance baseline. English and Vietnamese text synthesis, voice cloning, local HTTP API, and controlled benchmark are qualified.

### Single-T4 INT8 semantic + FP16 codec

Capacity-oriented fallback. The semantic checkpoint is weight-only INT8 while the codec remains FP16. It fits full TTS on one T4 but is slower than the dual-T4 FP16 semantic path.

### Two independent single-T4 INT8 instances

Concurrency-oriented mode. Each physical T4 runs one isolated API process. The clean-room acceptance reproduced approximately 2x aggregate request scaling for the tested deterministic short request.

## Source control and provenance

- Fish Speech runtime is pinned by commit SHA in `references/upstream.lock`.
- Fish Audio S2 Pro weights are mounted from the Kaggle model mirror and are never committed.
- VoxCPM2 is used only as an independent synthetic reference generator for the final multi-speaker voice-cloning gate.
- The verifier for speaker discrimination is pinned independently.

## Design principles

1. Prefer explicit placement over implicit framework device selection.
2. Fail early on unsupported or incomplete environments.
3. Keep model weights outside Git.
4. Separate technical acceptance from subjective claims.
5. Preserve authority evidence beside human-readable conclusions.
6. Re-run critical paths in a fresh Kaggle session before release.
7. Treat reproducibility defects discovered by clean-room testing as release-blocking code defects.

## Release boundary

The project demonstrates the tested Kaggle T4x2 configurations. It does not claim universal performance across arbitrary GPUs, universal equivalence between INT8 and FP16 audio quality, or universal speaker-cloning equivalence for arbitrary real-human voices.
