# Architecture

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](architecture.vi.md)

## Baseline dual-GPU topology

```text
cuda:0 / T4 16 GB
  Dual-AR / text-to-semantic
  KV cache

cuda:1 / T4 16 GB
  codec / decoder
  semantic codes -> waveform
```

Generated semantic codes must be explicitly moved to the decoder device before audio decode. Input tensors must follow the device of the model that consumes them; no code should rely on an implicit default CUDA device.
