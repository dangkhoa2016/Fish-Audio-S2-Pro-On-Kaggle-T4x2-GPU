# Phương pháp benchmark

> 🌐 Language / Ngôn ngữ: [English](benchmark-methodology.md) | **Tiếng Việt**

Correctness phải được qualification trước khi đo performance.

## Baseline

- precision: FP16
- batch: 1
- `max_seq_len`: 4096
- compile: OFF
- GPU0: Dual-AR / text-to-semantic
- GPU1: codec / decoder

## Metrics bắt buộc

- wall-clock inference time
- output audio duration
- RTF = inference_time / audio_duration
- peak VRAM của từng GPU
- output sample rate và byte size
- SHA-256 của retained output samples

Cold-start result và warm inference result phải được báo cáo riêng. Kết quả benchmark chỉ có ý nghĩa trong baseline đã khóa và không được suy rộng sang hardware hoặc configuration chưa kiểm tra.
