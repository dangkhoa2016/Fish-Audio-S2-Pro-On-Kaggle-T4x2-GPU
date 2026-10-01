# Fish Audio S2 Pro on Kaggle T4x2 — Project Contract

## Baseline
- Upstream runtime: official `fishaudio/fish-speech`
- Upstream revision: `214da3cd841bda85da2496b96cd3c4d7edb1337e`
- Original model: `fishaudio/s2-pro`
- Kaggle mirror: `dangkhoa2016/fishaudio-s2-pro`
- Precision: FP16
- Batch size: 1
- Baseline max sequence length: 4096
- torch.compile: OFF

## Target topology
- `cuda:0`: Dual-AR / text-to-semantic model and KV cache
- `cuda:1`: codec / reference encoder / decoder

## Required qualification
- Environment and two-T4 preflight PASS
- Official single-T4 baseline characterized
- Dual-T4 FP16 model load without OOM
- English and Vietnamese text-only synthesis PASS
- English and Vietnamese voice cloning PASS
- Valid non-empty WAV outputs
- Peak VRAM, latency, audio duration and RTF recorded
- Fresh Kaggle T4x2 clean-room regression PASS
- Reproducible synthetic multi-speaker gate: 8 speakers, same-language, cross-language and deterministic-repeat coverage
- Independent speaker-embedding analysis retained as supporting evidence
- Speaker verifier: `microsoft/wavlm-base-plus-sv` pinned to revision `feb593a6c23c1cc3d9510425c29b0a14d2b07b1e`
- Reproducible evidence retained under `evidence/`, `results/`, `assets/synthetic-speakers/` and `reports/`

## Synthetic final voice-cloning gate
- Independent reference generator: OpenBMB VoxCPM2
- 4 English + 4 Vietnamese synthetic speakers
- References are 10–30 seconds with known transcripts
- 8 same-language cases
- 4 cross-language cases
- 2 deterministic-repeat cases
- Real-human references are optional private extensions, not a release requirement

## Rules
- Do not commit model weights or secrets.
- Do not mislabel synthetic voices as real people.
- Do not claim synthetic-reference evaluation is universally equivalent to arbitrary real-human voices.
- Do not enable compile before correctness baseline passes.
- Quantized single-T4 and dual-instance work remain separate tracks.
