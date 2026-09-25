# Troubleshooting

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](troubleshooting.vi.md)

## Single T4 OOM
Treat a reproducible upstream OOM on 16 GB as an expected characterization result. Do not spend GPU quota repeatedly retrying the same uncontrolled configuration.

## Device mismatch
Log the device and dtype for each loaded component. Move generated codes explicitly to the decoder device before decode.

## Kaggle package drift
After the first GPU PASS, record Python, PyTorch, CUDA, driver and `pip freeze`, then pin the working environment.

## Compile problems
Keep `torch.compile` disabled until the correctness baseline passes.
