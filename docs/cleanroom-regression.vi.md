# Fresh Kaggle T4x2 Clean-Room Regression

> 🌐 Language / Ngôn ngữ: [English](cleanroom-regression.md) | **Tiếng Việt**

Status: **PASS**

## Mục tiêu

Reproduce các Fish Audio S2 Pro deployment paths đã chấp nhận từ một Kaggle T4x2 session mới, dùng attached Kaggle model mirror và pinned Fish Speech upstream revision.

## Environment

- 2 × NVIDIA Tesla T4 được PyTorch detect
- pinned upstream commit: `214da3cd841bda85da2496b96cd3c4d7edb1337e`
- Kaggle model mirror: `dangkhoa2016/fishaudio-s2-pro`
- `max_seq_len=4096`
- `torch.compile=OFF`
- model weights chỉ load từ Kaggle model attachment

## FP16 dual-GPU regression

Split topology reproduce thành công: GPU0 host semantic / Dual-AR / KV cache, GPU1 host codec / decoder. English full TTS, Vietnamese full TTS và local HTTP API đều PASS.

Retained CLI outputs:

- `results/cleanroom-regression/fp16-en-final.wav`
- `results/cleanroom-regression/fp16-vi-final.wav`

## INT8 single-T4 regression

Single-T4 INT8 conversion reproduce từ Kaggle model mount:

- `model.pth`: 5,078,844,907 bytes
- state tensors: 559
- INT8 tensors: 201
- BF16 tensors: 358
- không `model.safetensors.index.json`
- không giữ original FP16 semantic shards trong INT8 runtime directory

English và Vietnamese full TTS đều PASS trên một T4.

## Hai INT8 instance độc lập

Cả hai servers đạt health HTTP 200:

- GPU0 -> instance A -> `127.0.0.1:8091`
- GPU1 -> instance B -> `127.0.0.1:8092`

| Mode | A | B | Effective wall |
|---|---:|---:|---:|
| Single | 20.167 s | 18.079 s | — |
| Concurrent | 19.003 s | 17.926 s | 19.003 s |

Sequential sum là 38.246 s, vì vậy concurrent pair reproduce khoảng **2.01× aggregate scaling**. Peak monitored VRAM là 11,092.875 MiB trên mỗi GPU.

Single-A, single-B, parallel-A và parallel-B WAV đều 44.1 kHz mono, 258,092 bytes, 2.925714 s và cùng SHA-256 `cbdecdec91a4d39dd0ff535c964273f9f8e46d66d25db49b87b3767adb8ae968`.

## Corrective được clean-room test phát hiện

1. `scripts/apply_upstream_patch.sh` phải apply cumulative API dual-GPU patch thay vì earlier CLI-only patch.
2. CLI runners phải resolve relative output path trước khi đổi vào upstream checkout.
3. CLI runners phải yêu cầu output WAV tồn tại và non-empty trước khi báo PASS.

Output guard ngăn upstream inference traceback bị hiểu nhầm là success khi không có WAV.

## Acceptance

Clean-room regression được chấp nhận PASS.

Mandatory real-human gate sau đó được supersede bởi reproducible synthetic multi-speaker acceptance tại `docs/synthetic-multispeaker-voice-cloning-acceptance.md`.

Machine-readable results nằm tại `results/cleanroom-regression/summary.json`.
