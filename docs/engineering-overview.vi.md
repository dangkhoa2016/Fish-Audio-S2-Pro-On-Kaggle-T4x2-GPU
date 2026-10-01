# Tổng quan kỹ thuật

> 🌐 Language / Ngôn ngữ: [English](engineering-overview.md) | **Tiếng Việt**

## Mục tiêu

Chạy Fish Audio S2 Pro có khả năng tái lập trên môi trường Kaggle dual Tesla T4, đồng thời giữ đủ evidence để reviewer độc lập phân biệt measured behavior với assumption.

## Hardware model

Dự án không xem hai GPU T4 16 GB như 32 GB VRAM dùng chung. FP16 topology đã chấp nhận phân tách rõ:

- GPU0: text-to-semantic / Dual-AR model và KV cache.
- GPU1: codec, reference encoder và audio decoder.
- Precision: FP16.
- Batch size: 1.
- Maximum sequence length: 4096.
- `torch.compile`: disabled.

Đây là release baseline.

## Các operating mode được hỗ trợ

### Dual-T4 FP16

Quality/performance baseline chính. Đã qualification English/Vietnamese text synthesis, voice cloning, local HTTP API và controlled benchmark.

### Single-T4 semantic INT8 + codec FP16

Capacity-oriented fallback. Semantic checkpoint dùng weight-only INT8, codec vẫn FP16. Cấu hình này fit full TTS trên một T4 nhưng semantic path chậm hơn dual-T4 FP16.

### Hai single-T4 INT8 instance độc lập

Concurrency-oriented mode. Mỗi T4 vật lý chạy một API process độc lập. Clean-room acceptance tái lập xấp xỉ 2x aggregate request scaling cho deterministic short request đã kiểm tra.

## Source control và provenance

- Fish Speech runtime được pin bằng commit SHA trong `references/upstream.lock`.
- Fish Audio S2 Pro weights được mount từ Kaggle model mirror và không commit vào Git.
- VoxCPM2 chỉ dùng làm independent synthetic reference generator cho final multi-speaker voice-cloning gate.
- Speaker verifier được pin độc lập.

## Nguyên tắc thiết kế

1. Ưu tiên explicit placement thay vì implicit framework device selection.
2. Fail sớm với môi trường không hỗ trợ hoặc thiếu thành phần.
3. Giữ model weights ngoài Git.
4. Tách technical acceptance khỏi subjective claims.
5. Giữ authority evidence cạnh human-readable conclusions.
6. Chạy lại critical paths trong một Kaggle session mới trước release.
7. Xem reproducibility defect phát hiện bởi clean-room test là release-blocking code defect.

## Release boundary

Dự án chỉ chứng minh các Kaggle T4x2 configuration đã kiểm tra. Không tuyên bố universal performance trên arbitrary GPUs, universal quality equivalence giữa INT8 và FP16, hoặc universal speaker-cloning equivalence cho arbitrary real-human voices.
