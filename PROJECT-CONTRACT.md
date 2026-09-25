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
- `cuda:1`: codec / audio decoder

## Required qualification
- Environment and two-T4 preflight PASS
- Official single-T4 baseline characterized as PASS or EXPECTED-FAIL
- Dual-T4 FP16 model load without OOM
- English and Vietnamese text-only synthesis PASS
- English and Vietnamese same-language voice cloning usable
- Valid non-empty WAV outputs
- Peak VRAM per GPU, latency, audio duration and RTF recorded
- Reproducible evidence retained under `evidence/` and `results/`

## Rules
- Do not commit model weights or secrets.
- Do not enable compile before correctness baseline passes.
- Do not benchmark before dual-GPU correctness passes.
- Quantized single-T4 and dual-instance work are separate experimental tracks.
