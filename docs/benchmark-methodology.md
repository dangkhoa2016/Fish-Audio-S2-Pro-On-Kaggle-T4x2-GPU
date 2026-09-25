# Benchmark methodology

Correctness is qualified before performance measurement.

Baseline dimensions:
- precision: FP16
- batch: 1
- max_seq_len: 4096
- compile: OFF
- GPU0: Dual-AR/text-to-semantic
- GPU1: codec/decoder

Required metrics:
- wall-clock inference time
- output audio duration
- RTF = inference_time / audio_duration
- peak VRAM for each GPU
- output sample rate and byte size
- SHA-256 for retained output samples

Cold-start results and warm inference results must be reported separately.
