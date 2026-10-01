# v1.0.0 Release Notes

Initial public release of the reproducible Fish Audio S2 Pro Kaggle T4x2 inference project.

## Highlights

- Dual-T4 FP16 split inference for Fish Audio S2 Pro.
- English text-to-speech qualification plus technical Vietnamese pipeline qualification; native Vietnamese pronunciation quality is explicitly not qualified.
- Local HTTP API qualification.
- Canonical bilingual Kaggle production notebook with fresh T4x2 technical Run All acceptance and a reviewer-facing reference-conditioned listening path.
- Controlled benchmark with retained evidence.
- Single-T4 INT8 semantic + FP16 codec path.
- Two independent single-T4 INT8 instances running concurrently on Kaggle T4x2.
- Fresh-session clean-room regression.
- Reproducible synthetic multi-speaker voice-cloning acceptance using an independent VoxCPM2 reference bank.
- 8 synthetic speakers, 12 clone cases, and 2 deterministic repeats.
- Independent WavLM speaker verification: 12 / 12 outputs ranked the intended reference speaker top-1.
- Side-by-side HTML listening report.

## Locked baseline

- Hardware: 2 × NVIDIA Tesla T4 16 GB.
- Semantic model: GPU0.
- Codec / reference encoder / decoder: GPU1.
- Precision: FP16.
- Batch size: 1.
- max_seq_len: 4096.
- torch.compile: OFF.
- Fish Speech upstream pin: 214da3cd841bda85da2496b96cd3c4d7edb1337e.

## Kaggle production notebook

The canonical notebook completed a fresh Kaggle **GPU T4 x2** Run All for the engineering paths: six reference-free bilingual cases, the 12-case VoxCPM2-conditioned S2 Pro matrix, four cross-language cases, and local API English/Vietnamese requests all completed successfully.

Human listening during pre-public review established a separate language-quality boundary. Reference-free Vietnamese sounded noticeably non-native. Repeating the test with same-language VoxCPM2 Vietnamese references improved the result only modestly; pronunciation and tonal realization still did not sound like native Vietnamese speech. No corresponding CUDA, memory, HTTP API, or split-device runtime failure was observed.

Accordingly, v1.0.0 claims **Vietnamese pipeline compatibility**, not native Vietnamese pronunciation quality:

```text
VIETNAMESE_PIPELINE_COMPATIBILITY=PASS
VIETNAMESE_NATIVE_PRONUNCIATION=NOT_QUALIFIED
KAGGLE_PRODUCTION_DEMO_TECHNICAL=PASS
```

The retained technical logs remain valid engineering evidence. Human listening defines the language-quality boundary rather than invalidating those runtime measurements.

## Important limitations

- Full FP16 TTS does not fit on one T4 in the tested configuration.
- Single-T4 INT8 semantic inference is slower than the FP16 semantic baseline.
- Synthetic multi-speaker acceptance does not claim universal equivalence to arbitrary real-human voice evaluation.
- Vietnamese generation and conditioning are technically functional, but native Vietnamese pronunciation / tonal naturalness is **NOT QUALIFIED**.
- WebUI and public tunnel deployment are outside the qualified baseline.
- Model weights are not included in this repository.

## Licensing

Original repository-authored code and documentation are released under the MIT License; see `LICENSE`. The MIT copyright holder is `Đăng Khoa <i.am@dangkhoa.dev>`.

Fish Audio S2 Pro model weights, upstream Fish Speech source, and patch artifacts that modify Fish Speech are not relicensed under MIT. They remain governed by the Fish Audio Research License. See `LICENSE-NOTES.md`, `NOTICE.txt`, `patches/README.md`, and `THIRD_PARTY_LICENSES/FISH-AUDIO-RESEARCH-LICENSE`.

**Built with Fish Audio.** Commercial use of Fish Audio Materials or Derivative Works requires a separate written license from Fish Audio under the retained license terms.

The independent VoxCPM2 reference generator is recorded in `references/synthetic-reference-source.md`.

## Release authority

See `docs/final-release-readiness.md`, `docs/qualification-matrix.md`, `docs/evidence-index.md`, and the retained `evidence/` / `results/` directories for the release qualification record.

## Release artifacts

The release publishes a qualification-artifacts archive built from the final tagged repository state. Model weights are excluded.

- `Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU-v1.0.0-qualification-artifacts.tar.gz` — retained evidence, machine-readable results, reviewer reports, bilingual documentation, provenance records, patch artifacts, licensing materials, release authority records, and an internal SHA-256 manifest.
- `Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU-v1.0.0-qualification-artifacts.tar.gz.sha256` — SHA-256 checksum for the archive.

The archive is intended for independent review and reproducibility auditing. It does not contain Fish Audio S2 Pro model weights.
