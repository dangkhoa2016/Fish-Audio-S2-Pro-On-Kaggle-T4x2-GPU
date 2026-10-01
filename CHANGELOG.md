# Changelog

All notable repository-level changes are documented here.

## v1.0.0 — 2026-10-01

### Added
- Reproducible dual-T4 FP16 Fish Audio S2 Pro runtime for Kaggle.
- English and Vietnamese synthesis and voice-cloning qualification.
- Local API qualification and controlled benchmark.
- Bilingual Kaggle production notebook with fresh T4x2 Run All acceptance.
- Single-T4 INT8 semantic + FP16 codec operating mode.
- Two-instance T4x2 INT8 concurrency mode.
- Fresh-session clean-room regression and corrective fixes.
- VoxCPM2 synthetic eight-speaker reference bank.
- Same-language and cross-language multi-speaker acceptance.
- Independent WavLM top-1 speaker verification and deterministic-repeat checks.
- Retained evidence, machine-readable summaries, audio outputs, and listening report.
- Licensing, NOTICE, release audit, and reviewer documentation.

### Release baseline
- 2 × NVIDIA Tesla T4 16 GB.
- FP16 split topology with semantic model on GPU0 and codec/decode on GPU1.
- batch size 1, max_seq_len 4096, torch.compile disabled.
- Fish Speech pinned to commit `214da3cd841bda85da2496b96cd3c4d7edb1337e`.

### Scope
This release documents only the tested configurations and does not claim universal hardware performance, universal INT8/FP16 subjective equivalence, or universal cloning equivalence for arbitrary real-human voices.
