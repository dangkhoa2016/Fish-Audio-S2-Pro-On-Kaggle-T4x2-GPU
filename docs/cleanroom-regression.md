# Fresh Kaggle T4x2 Clean-Room Regression

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](cleanroom-regression.vi.md)

Status: **PASS**

## Objective

Reproduce the accepted Fish Audio S2 Pro deployment paths from a fresh Kaggle T4x2 session using the repository at the productization-audit baseline commit `1bb0e4b8832f6563f17bd743ff94b21b0128d49c`, the attached Kaggle model mirror, and the pinned Fish Speech upstream revision.

## Environment

- 2 × NVIDIA Tesla T4 detected by PyTorch
- pinned upstream commit: `214da3cd841bda85da2496b96cd3c4d7edb1337e`
- Kaggle model mirror: `dangkhoa2016/fishaudio-s2-pro`
- `max_seq_len=4096`
- `torch.compile=OFF`
- model weights loaded only from the Kaggle model attachment

## FP16 dual-GPU regression

The split topology reproduced successfully: GPU0 hosts semantic / Dual-AR / KV cache and GPU1 hosts codec / decoder. English full TTS, Vietnamese full TTS, and the local HTTP API all passed.

The final retained CLI outputs are `results/cleanroom-regression/fp16-en-final.wav` and `fp16-vi-final.wav`.

## INT8 single-T4 regression

The single-T4 INT8 conversion reproduced from the Kaggle model mount:

- `model.pth`: 5,078,844,907 bytes
- state tensors: 559
- INT8 tensors: 201
- BF16 tensors: 358
- no `model.safetensors.index.json`
- no original FP16 semantic shards in the INT8 runtime directory

English and Vietnamese full TTS both passed on one T4.

## Two independent INT8 instances

Both independent servers reached health HTTP 200:

- GPU0 -> instance A -> `127.0.0.1:8091`
- GPU1 -> instance B -> `127.0.0.1:8092`

| Mode | A | B | Effective wall |
|---|---:|---:|---:|
| Single | 20.167 s | 18.079 s | — |
| Concurrent | 19.003 s | 17.926 s | 19.003 s |

The measured sequential sum is 38.246 s, so the concurrent pair reproduced approximately **2.01× aggregate scaling** for this clean-room sample. Peak monitored VRAM was 11,092.875 MiB on each GPU.

The single-A, single-B, parallel-A and parallel-B WAVs are all 44.1 kHz mono, 258,092 bytes, 2.925714 s, and share SHA-256 `cbdecdec91a4d39dd0ff535c964273f9f8e46d66d25db49b87b3767adb8ae968`.

## Correctives discovered by clean-room testing

1. `scripts/apply_upstream_patch.sh` must apply the cumulative API dual-GPU patch rather than the earlier CLI-only patch.
2. CLI runners must resolve relative output paths before changing into the upstream checkout.
3. CLI runners must require a non-empty output WAV before reporting PASS.

The output guard prevents an upstream inference traceback from being mistaken for a successful qualification when no WAV was produced.

## Acceptance

The clean-room regression is accepted as PASS.

No `v1.0.0` tag was created during this regression run. The later release policy superseded the mandatory real-human gate with the reproducible synthetic multi-speaker acceptance documented in `docs/synthetic-multispeaker-voice-cloning-acceptance.md`.

Machine-readable results are retained in `results/cleanroom-regression/summary.json`.
