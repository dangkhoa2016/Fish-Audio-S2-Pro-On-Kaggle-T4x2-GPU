# Qualification Single-T4 INT8

> 🌐 Language / Ngôn ngữ: [English](single-t4-int8.md) | **Tiếng Việt**

Status: **PASS**

## Mục tiêu

Xác định full Fish Audio S2 Pro TTS pipeline có thể fit trên một Kaggle Tesla T4 16 GB sau khi quantize semantic model hay không, trong khi codec vẫn FP16.

Đây là capacity-oriented configuration riêng, không thay thế official dual-T4 FP16 baseline.

## Cấu hình

- Semantic model: upstream weight-only INT8
- Codec: FP16
- Runtime: FP16
- Batch size: 1
- `max_seq_len`: 4096
- `torch.compile`: OFF
- Semantic device: `cuda:0`
- Decoder device: `cuda:0`
- Physical GPUs per instance: 1

Upstream INT8 path được chọn bằng checkpoint path có `int8` và thay Linear layers bằng weight-only INT8 modules.

## Quantized checkpoint

Runtime checkpoint được tạo tại `/tmp/fish-s2-pro-int8`.

- `model.pth`: 5,078,844,907 bytes
- State tensors: 559
- INT8 tensors: 201
- BF16 tensors: 358
- Source model load: 69.975 s
- Total conversion: 208.239 s
- Không giữ safetensors index trong INT8 directory
- `codec.pth` được link từ original Kaggle model mount

Checkpoint khoảng 5 GB này cố ý không commit vào Git.

- Conversion script: `scripts/quantize_single_t4_int8.py`
- Full-TTS runner: `scripts/run_single_t4_int8.sh`

## Kết quả

| Test | Result | Semantic tok/s | Audio |
|---|---|---:|---:|
| INT8 semantic-only EN | PASS | 3.65 | — |
| INT8 full TTS EN | PASS | 3.75 | 2.926 s |
| INT8 full TTS VI | PASS | 3.73 | 4.412 s |

Hai retained WAV đều mono PCM 44.1 kHz, clipping ratio 0.

Memory trong Vietnamese full-pipeline run:

- semantic-side reported memory: ~7.09 GB
- allocated after codec decode: 10.983 GB
- reserved after codec decode: 11.494 GB
- peak allocated: 11.246 GB
- peak reserved: 11.494 GB

Cùng full FP16 pipeline trước đó OOM trên một T4 sau semantic generation khi codec bắt đầu load.

## Trade-off so với FP16

Memory giảm đáng kể, nhưng upstream weight-only INT8 chậm hơn trong configuration này.

- FP16 single-T4 characterization: ~8.18 tokens/s
- INT8 single-T4: ~3.65–3.75 tokens/s

INT8 implementation dequantize/cast weights trong Linear forward, nên đây chủ yếu là capacity-enabling configuration, không phải speed optimization.

## Acceptance scope

Qualification này chứng minh complete technical TTS pipeline chạy được trên một Kaggle T4 với semantic INT8 + codec FP16. Không tuyên bố subjective audio-quality equivalence với FP16 baseline.

Artifacts:

- `results/single-t4-int8/summary.json`
- `results/single-t4-int8/en-sample.wav`
- `results/single-t4-int8/vi-sample.wav`
- `evidence/single-t4-int8-convert.log`
- `evidence/single-t4-int8-semantic.log`
- `evidence/single-t4-int8-en.log`
- `evidence/single-t4-int8-vi.log`

Kết quả này cho phép triển khai dual-instance concurrency: một independent single-T4 instance trên mỗi GPU vật lý.
