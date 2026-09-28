# Fish Audio S2 Pro trên Kaggle T4x2 GPU

> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

[![Repository Audit](https://github.com/dangkhoa2016/Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/dangkhoa2016/Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Release](https://img.shields.io/badge/release-v1.0.0-blue)
![Hardware](https://img.shields.io/badge/Kaggle-T4%20x2-20BEFF)
![Runtime](https://img.shields.io/badge/Fish%20Speech-pinned-success)

Triển khai Fish Audio S2 Pro có khả năng tái lập trên Kaggle bằng hai GPU NVIDIA Tesla T4 16 GB, với cách phân bổ rõ ràng từng thành phần model lên từng GPU.


## Trạng thái

All qualified runtime and release paths đã hoàn thành. Baseline FP16 dual-GPU đã PASS, single-T4 INT8 qualification chứng minh full TTS với semantic INT8 + codec FP16 có thể chạy trên một Tesla T4, dual-instance concurrency qualification chứng minh hai instance single-T4 INT8 độc lập có thể chạy đồng thời trên Kaggle T4x2, và clean-room regression đã tái lập các đường chạy đã chấp nhận từ một Kaggle T4x2 session hoàn toàn mới.

Dự án đã **đạt điều kiện release v1.0.0**. Fresh clean-room regression, synthetic multi-speaker voice-cloning acceptance có thể tái lập, objective speaker verification và final release-readiness audit đều đã PASS.

## Hướng dẫn review

Để review dự án theo cấu trúc kỹ thuật, hãy bắt đầu từ:

- [Documentation guide](docs/README.md)
- [Engineering overview](docs/engineering-overview.md)
- [Qualification matrix](docs/qualification-matrix.md)
- [Reproducibility guide](docs/reproducibility.md)
- [Evidence index](docs/evidence-index.md)
- [Development history](docs/development-history.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Citation](CITATION.cff)

## Topology đã xác nhận

- `cuda:0`: Dual-AR / text-to-semantic / KV cache
- `cuda:1`: codec / reference encoder / audio decoder
- precision: FP16
- batch size: 1
- `max_seq_len`: 4096
- `torch.compile`: OFF

Hai T4 không được xem như một GPU 32 GB VRAM. Pipeline được phân tách thành các thành phần và đặt trực tiếp lên từng GPU.

## Model và mã nguồn

- Model gốc: `fishaudio/s2-pro`
- Kaggle mirror: `dangkhoa2016/fishaudio-s2-pro`
- Runtime source: official `fishaudio/fish-speech`
- Upstream revision đã pin: `214da3cd841bda85da2496b96cd3c4d7edb1337e`

Xem `references/upstream.lock` và `references/model-source.md`.

## Các mốc đã xác nhận

| Hạng mục | Kết quả |
|---|---|
| Kaggle T4x2 CUDA preflight | PASS |
| Single-T4 semantic generation | PASS |
| Single-T4 full FP16 TTS | Expected OOM |
| Single-T4 semantic INT8 + codec FP16 | PASS |
| Hai instance single-T4 INT8 độc lập | PASS |
| Dual-T4 FP16 CLI TTS | PASS |
| Tổng hợp tiếng Anh | PASS |
| Tổng hợp tiếng Việt | PASS |
| Voice cloning kỹ thuật | PASS |
| Local HTTP API | PASS |
| Controlled benchmark | PASS |
| Fresh Kaggle T4x2 clean-room regression | PASS |
| Synthetic multi-speaker voice cloning (8 speaker / 12 clone + 2 repeat) | PASS |
| Independent speaker-embedding top-1 (same / cross language) | 8/8 / 4/4 |

Gate voice cloning cuối cùng dùng speaker bank synthetic độc lập từ VoxCPM2. Cả 8/8 case same-language và 4/4 case cross-language đều xếp đúng speaker mục tiêu ở top-1 trong 8 reference bằng speaker encoder độc lập. Xem `docs/synthetic-multispeaker-voice-cloning-acceptance.md`.

## Controlled benchmark

Baseline: FP16, batch 1, `max_seq_len=4096`, compile OFF, 2 warmup, 8 scenario, mỗi scenario 5 lần đo.

| Scenario | Median wall | Median audio | Median RTF | Semantic tok/s |
|---|---:|---:|---:|---:|
| EN short | 13.194 s | 4.923 s | 2.720 | 8.276 |
| VI short | 12.869 s | 4.737 s | 2.698 | 8.361 |
| EN medium | 36.011 s | 13.653 s | 2.644 | 8.335 |
| VI medium | 35.111 s | 13.189 s | 2.644 | 8.308 |
| EN long | 58.209 s | 22.245 s | 2.617 | 8.297 |
| VI long | 57.921 s | 22.245 s | 2.604 | 8.338 |
| Clone EN | 12.384 s | 4.505 s | 2.749 | 8.217 |
| Clone VI | 10.361 s | 3.715 s | 2.800 | 8.156 |

Cold model-ready khoảng 96.709 giây. GPU0 giữ quanh 10.9 GB allocated; GPU1 khoảng 4.4–5.5 GB. Không có OOM hoặc clipping trong 40 lần đo.

Xem `docs/benchmark-methodology.md` và `docs/controlled-benchmark-results.md` để biết phương pháp và kết quả đầy đủ. Kết quả single-T4 INT8 nằm tại `docs/single-t4-int8.md`. Kết quả hai instance độc lập nằm tại `docs/dual-instance-concurrency.md`.

## Tái lập

Repo chứa các script và patch đã dùng trong qualification:

1. `scripts/bootstrap_kaggle.sh`
2. `scripts/preflight.sh`
3. `scripts/setup_runtime.sh`
4. `scripts/inventory_model.py`
5. `scripts/apply_upstream_patch.sh`
6. `scripts/run_dual_gpu_fp16.sh`
7. `scripts/qualify_text_synthesis.py`
8. `scripts/qualify_voice_cloning.py`
9. `scripts/run_api_server_dual_gpu.sh`
10. `scripts/run_controlled_benchmark.py`
11. `scripts/quantize_single_t4_int8.py`
12. `scripts/run_single_t4_int8.sh`
13. `scripts/run_api_server_single_t4_int8.sh`
14. `scripts/setup_voxcpm2_reference_runtime.sh`
15. `scripts/generate_synthetic_speaker_bank.py`
16. `scripts/qualify_synthetic_multispeaker.py`
17. `scripts/score_synthetic_speakers.py`
18. `scripts/check_synthetic_repeatability.py`
19. `scripts/build_synthetic_review_html.py`

Với session mới, bắt đầu bằng `scripts/bootstrap_kaggle.sh`; script này checkout chính xác upstream commit từ `references/upstream.lock` và inventory Kaggle model đã attach. Sau đó chạy preflight, runtime setup, apply patch và runner qualification tương ứng.

Các lệnh khởi động chính xác cho hai instance dual-instance concurrency qualification được ghi tại `docs/dual-instance-concurrency.md`.

Patch nằm trong `patches/`. Evidence runtime và output mẫu được giữ trong `evidence/` và `results/`.

Synthetic multi-speaker voice-cloning acceptance được mô tả tại `docs/synthetic-multispeaker-voice-cloning-acceptance.md`. Nguồn reference được ghi tại `references/synthetic-reference-source.md`; `reports/synthetic-multispeaker-review.html` hỗ trợ nghe so sánh trực tiếp.

## Giới hạn hiện tại

- Full FP16 TTS không fit trên một T4 với upstream configuration đã kiểm tra.
- `max_seq_len=4096` được chọn có chủ đích, thấp hơn cấu hình upstream S2 Pro là 32768.
- WebUI chưa được build/qualification.
- Chưa có public tunnel test.
- Gate release cuối dùng synthetic references có thể tái lập; kết quả này không được diễn giải thành tương đương tuyệt đối với mọi giọng người thật.
- Semantic INT8 chậm hơn FP16 và chưa tuyên bố tương đương chất lượng nghe chủ quan.
- `torch.compile` không thuộc baseline.

## License

Repo không chứa model weights. Xem `LICENSE-NOTES.md` và license của upstream/model trước khi sử dụng hoặc phân phối lại.

## Project contract

Xem `PROJECT-CONTRACT.md` để biết baseline đã khóa và acceptance criteria. Final release audit: `docs/final-release-readiness.md`.
