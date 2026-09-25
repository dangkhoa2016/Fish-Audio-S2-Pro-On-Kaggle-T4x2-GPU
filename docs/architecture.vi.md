# Kiến trúc

> 🌐 Language / Ngôn ngữ: [English](architecture.md) | **Tiếng Việt**

## Topology dual-GPU baseline

```text
cuda:0 / T4 16 GB
  Dual-AR / text-to-semantic
  KV cache

cuda:1 / T4 16 GB
  codec / decoder
  semantic codes -> waveform
```

Semantic codes được sinh ra phải được chuyển tường minh sang thiết bị của decoder trước khi audio decode. Input tensor phải đi theo đúng device của model component sử dụng nó; code không được dựa vào một CUDA device mặc định ngầm định.

Hai GPU T4 không được xem như một GPU 32 GB VRAM dùng chung. Baseline đã qualification dùng explicit component placement giữa hai GPU.
