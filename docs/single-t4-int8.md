# Single-T4 INT8 Qualification

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](single-t4-int8.vi.md)

Status: **PASS**

## Objective

Determine whether the complete Fish Audio S2 Pro TTS pipeline can fit on one Kaggle Tesla T4 16 GB GPU after quantizing the semantic model, while keeping the codec in FP16.

This experiment is separate from the official FP16 dual-T4 baseline.

## Configuration

- Semantic model: upstream weight-only INT8
- Codec: FP16
- Runtime: FP16
- Batch size: 1
- max_seq_len: 4096
- torch.compile: OFF
- Semantic device: cuda:0
- Decoder device: cuda:0
- Physical GPUs used per instance: 1

The upstream INT8 path is selected by an `int8` checkpoint path and replaces Linear layers with weight-only INT8 modules.

## Quantized checkpoint

The runtime checkpoint was generated under `/tmp/fish-s2-pro-int8`.

- `model.pth`: 5,078,844,907 bytes
- State tensors: 559
- INT8 tensors: 201
- BF16 tensors: 358
- Source model load: 69.975 s
- Total conversion: 208.239 s
- No safetensors index is retained in the INT8 directory
- `codec.pth` is linked from the original Kaggle model mount

The 5 GB quantized checkpoint is intentionally not committed to Git.

Reproduction script: `scripts/quantize_single_t4_int8.py`
Full-TTS runner: `scripts/run_single_t4_int8.sh`

## Results

| Test | Result | Semantic tok/s | Audio |
|---|---|---:|---:|
| INT8 semantic-only EN | PASS | 3.65 | — |
| INT8 full TTS EN | PASS | 3.75 | 2.926 s |
| INT8 full TTS VI | PASS | 3.73 | 4.412 s |

Both retained WAV samples are mono PCM at 44.1 kHz and have clipping ratio 0.

Measured memory during the Vietnamese full-pipeline run:

- semantic-side reported memory: ~7.09 GB
- allocated after codec decode: 10.983 GB
- reserved after codec decode: 11.494 GB
- peak allocated: 11.246 GB
- peak reserved: 11.494 GB

The same full FP16 pipeline previously OOMed on one T4 after semantic generation when the codec attempted to load.

## Trade-off versus FP16

The memory reduction is substantial, but upstream weight-only INT8 is slower in this configuration.

- FP16 single-T4 characterization: ~8.18 tokens/s
- INT8 single-T4: ~3.65–3.75 tokens/s

The INT8 implementation dequantizes/casts weights during Linear forwards, so this is primarily a capacity-enabling configuration, not a speed optimization.

## Acceptance scope

This qualification proves that the complete technical TTS pipeline can run on one Kaggle T4 with this INT8 semantic + FP16 codec configuration.
It does **not** claim subjective audio-quality equivalence to the FP16 baseline. Human listening comparison remains a separate quality task.

Artifacts:

- `results/single-t4-int8/summary.json`
- `results/single-t4-int8/en-sample.wav`
- `results/single-t4-int8/vi-sample.wav`
- `evidence/single-t4-int8-convert.log`
- `evidence/single-t4-int8-semantic.log`
- `evidence/single-t4-int8-en-full.log`
- `evidence/single-t4-int8-vi-full.log`

Successful single-T4 qualification enables the dual-instance concurrency configuration: one independent single-T4 instance per physical GPU.
