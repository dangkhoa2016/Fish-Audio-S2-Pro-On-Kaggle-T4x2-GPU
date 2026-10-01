# Fish Audio S2 Pro trên Kaggle T4x2 GPU

> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

[![Repository Audit](https://github.com/dangkhoa2016/Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/dangkhoa2016/Fish-Audio-S2-Pro-On-Kaggle-T4x2-GPU/actions/workflows/repository-audit.yml)
[![Original repository code: MIT](https://img.shields.io/badge/original%20repository%20code-MIT-yellow.svg)](LICENSE)
[![Fish Audio materials: Research License](https://img.shields.io/badge/Fish%20Audio%20materials-Research%20License-orange.svg)](THIRD_PARTY_LICENSES/FISH-AUDIO-RESEARCH-LICENSE)
![Release](https://img.shields.io/badge/release-v1.0.0-blue)
![Hardware](https://img.shields.io/badge/Kaggle-T4%20x2-20BEFF)
![Runtime](https://img.shields.io/badge/Fish%20Speech-pinned-success)

**Built with Fish Audio.**

Triển khai S2 Pro có khả năng tái lập trên Kaggle bằng hai GPU NVIDIA Tesla T4 16 GB, với cách phân bổ rõ ràng từng thành phần model lên từng GPU.

Repository này được xây dựng như một dự án qualification kỹ thuật thay vì một notebook chạy thử một lần. Nó kết hợp runtime implementation, clean-room reproducibility, retained evidence, controlled benchmark, independent speaker verification, repository governance và release documentation để các technical claims có thể được review trực tiếp dựa trên artifact cụ thể.

## Trạng thái

All qualified runtime and release paths đã hoàn thành. Baseline FP16 dual-GPU đã PASS, single-T4 INT8 qualification chứng minh full TTS với semantic INT8 + codec FP16 có thể chạy trên một Tesla T4, dual-instance concurrency qualification chứng minh hai instance single-T4 INT8 độc lập có thể chạy đồng thời trên Kaggle T4x2, và clean-room regression đã tái lập các đường chạy đã chấp nhận từ một Kaggle T4x2 session hoàn toàn mới.

Dự án đã **đạt điều kiện release v1.0.0**. Fresh clean-room regression, synthetic multi-speaker voice-cloning acceptance có thể tái lập, objective speaker verification và final release-readiness audit đều đã PASS.

### Các năng lực chính

- Dual-T4 FP16 inference với explicit component placement.
- English text synthesis cùng technical Vietnamese synthesis cho short, medium, long và expressive cases; native Vietnamese pronunciation chưa được qualification.
- Same-language và cross-language voice cloning.
- Local HTTP API qualification.
- Controlled FP16 benchmark với machine-readable results được lưu lại.
- Single-T4 semantic INT8 với codec FP16.
- Hai INT8 instance độc lập trên T4x2 cho concurrency scaling.
- Fresh-session clean-room regression.
- Independent VoxCPM2 synthetic reference bank và WavLM speaker verification.
- Deterministic repeatability checks và side-by-side listening report.

## Tài liệu

Root README là project overview. Khi review kỹ thuật, tái lập kết quả hoặc truy vết claim tới evidence, hãy dùng bộ tài liệu bên dưới.

### Bắt đầu từ đây

- [Documentation guide](docs/README.md) — navigation cho reviewer và operator.
- [Engineering overview](docs/engineering-overview.md) — system boundaries, hardware topology, operating modes và release scope.
- [Qualification matrix](docs/qualification-matrix.md) — capability, hardware, configuration, result và authority artifact.
- [Reproducibility guide](docs/reproducibility.md) — fresh-session procedure và acceptance rules.
- [Evidence index](docs/evidence-index.md) — ánh xạ claims tới logs, JSON summaries, WAV outputs và reports.
- [Development history](docs/development-history.md) — engineering narrative theo thời gian và các corrective discoveries.

### Architecture và methodology

- [Architecture](docs/architecture.md)
- [Benchmark methodology](docs/benchmark-methodology.md)
- [Troubleshooting](docs/troubleshooting.md)

### Qualification records

- [bilingual text-synthesis qualification — EN/VI text-only qualification](docs/bilingual-text-synthesis.md)
- [technical voice-cloning qualification — synthetic-reference voice cloning](docs/technical-voice-cloning.md)
- [local API qualification — local API qualification](docs/local-api-qualification.md)
- [controlled benchmark — controlled benchmark](docs/controlled-benchmark-results.md)
- [single-T4 INT8 qualification — single-T4 INT8](docs/single-t4-int8.md)
- [dual-instance concurrency qualification — two independent INT8 instances](docs/dual-instance-concurrency.md)
- [release/productization audit — release/productization audit](docs/release-productization-audit.md)
- [clean-room regression — fresh clean-room regression](docs/cleanroom-regression.md)
- [Synthetic multi-speaker voice-cloning acceptance](docs/synthetic-multispeaker-voice-cloning-acceptance.md)
- [Final release readiness](docs/final-release-readiness.md)

### Repository governance

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Citation metadata](CITATION.cff)
- [Project contract](PROJECT-CONTRACT.md)

## Topology đã xác nhận

- `cuda:0`: Dual-AR / text-to-semantic / KV cache
- `cuda:1`: codec / reference encoder / audio decoder
- precision: FP16
- batch size: 1
- `max_seq_len`: 4096
- `torch.compile`: OFF

Hai T4 không được xem như một GPU 32 GB VRAM. Pipeline được phân tách thành các thành phần và đặt trực tiếp lên từng GPU.

### Các operating mode đã qualification

**Dual-T4 FP16** là quality/performance baseline chính cho bilingual synthesis, cloning, local API serving và benchmark.

**Single-T4 semantic INT8 + codec FP16** là capacity-oriented fallback. Cấu hình này chạy complete TTS trên một Tesla T4, nhưng semantic path đo được chậm hơn FP16 và không được trình bày như speed optimization.

**Hai single-T4 INT8 instance độc lập** dùng một isolated process trên mỗi GPU. Clean-room concurrency rerun tái lập khoảng `2.0126x` aggregate scaling cho deterministic request đã kiểm tra. Đây là process-level parallelism, không phải pooled model memory.

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

### Independent voice-cloning verification

Final gate chủ đích tránh circular self-reference: S2 Pro không tự tạo reference bank dùng để đánh giá chính S2 Pro.

1. VoxCPM2 tạo tám synthetic reference speakers: bốn English và bốn Vietnamese.
2. S2 Pro tạo tám same-language và bốn cross-language clone cases.
3. Một WavLM-based speaker encoder độc lập so sánh từng clone với toàn bộ tám references.
4. Intended reference speaker đứng top-1 trong `12/12` cases.
5. Hai deterministic repeats được generate lại và kiểm tra byte-for-byte.

Measured verification summary:

```text
top-1 intended speaker    12 / 12
mean intended cosine      ~0.96917
mean impostor margin      ~0.14344
repeatability             2 / 2 byte-identical
```

Kết quả này chứng minh speaker-conditioning behavior có khả năng tái lập trên synthetic bank đã kiểm tra; nó không tuyên bố universal equivalence cho arbitrary real-human voices.

### Ranh giới phát âm tiếng Việt

Vietnamese pipeline hoạt động về mặt kỹ thuật: reference-free generation, same-language VoxCPM2 reference conditioning, cross-language conditioning và local API requests đều chạy thành công trên qualified T4x2 runtime. Tuy nhiên human listening ngày 2026-10-01 cho thấy tiếng Việt vẫn nghe rõ ràng chưa tự nhiên như người Việt bản ngữ, và same-language VoxCPM2 conditioning chỉ cải thiện ở mức nhỏ.

Vì vậy v1.0.0 chỉ claim **Vietnamese pipeline compatibility**, không claim native Vietnamese pronunciation hoặc tonal naturalness:

```text
VIETNAMESE_PIPELINE_COMPATIBILITY=PASS
VIETNAMESE_NATIVE_PRONUNCIATION=NOT_QUALIFIED
```

Không quan sát thấy lỗi tương ứng ở CUDA, memory, API hoặc split-device execution. Trong release này, behavior được xem là tested model-capability limitation thay vì Kaggle T4x2 integration defect.

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

Phần tái lập được tách thành tài liệu riêng để root README tập trung vào phạm vi dự án, kết quả đã xác nhận và các operating mode.

Xem **[Reproducibility Guide](docs/reproducibility.md)** để biết môi trường Kaggle cần thiết, clean-session contract, bootstrap sequence chính xác, ý nghĩa và mục đích của từng reproduction/qualification script, input/output dự kiến, workflow cho từng operating mode, vị trí evidence và acceptance rules.

Để dùng entry point Kaggle tương tác, hãy mở **[`notebooks/kaggle-production-demo.ipynb`](notebooks/kaggle-production-demo.ipynb)** với **GPU T4 x2** và model `dangkhoa2016/fishaudio-s2-pro` đã attach. Notebook giữ six-case EN/VI run làm technical baseline và dùng independent VoxCPM2 speaker bank làm conditioning evidence. Final scorecard tách rõ Vietnamese technical compatibility khỏi native-pronunciation quality; các marker `PASS` không được diễn giải thành native Vietnamese accent validation.

## Repository audit

Chạy cùng lightweight repository audit được mirror bởi GitHub Actions bằng:

```bash
make audit
```

Audit kiểm tra shell syntax, Python compilation, JSON validity, whitespace, model weights vô tình bị track và common secret-pattern checks.

## Giới hạn hiện tại

- Full FP16 TTS không fit trên một T4 với upstream configuration đã kiểm tra.
- `max_seq_len=4096` được chọn có chủ đích, thấp hơn cấu hình upstream S2 Pro là 32768.
- WebUI chưa được build/qualification.
- Chưa có public tunnel test.
- Gate release cuối dùng synthetic references có thể tái lập; kết quả này không được diễn giải thành tương đương tuyệt đối với mọi giọng người thật.
- Vietnamese generation và conditioning hoạt động về mặt kỹ thuật, nhưng native Vietnamese pronunciation / tonal naturalness là **NOT QUALIFIED**.
- Semantic INT8 chậm hơn FP16 và chưa tuyên bố tương đương chất lượng nghe chủ quan.
- `torch.compile` không thuộc baseline.

## License

Code và documentation nguyên bản được viết riêng cho repository được cấp phép theo [MIT License](LICENSE), ngoại trừ những file có nguồn gốc từ hoặc trực tiếp sửa đổi Fish Audio materials:

```text
Copyright (c) 2026 Đăng Khoa <i.am@dangkhoa.dev>
```

Fish Audio S2 Pro model weights, upstream Fish Speech code và các patch artifacts trong repository trực tiếp sửa Fish Speech vẫn chịu **Fish Audio Research License** và **không** được relicensed theo MIT.

Phạm vi patch và ranh giới license được mô tả tại [patches/README.md](patches/README.md). Xem thêm [LICENSE-NOTES.md](LICENSE-NOTES.md), [NOTICE.txt](NOTICE.txt) và [retained Fish Audio Research License](THIRD_PARTY_LICENSES/FISH-AUDIO-RESEARCH-LICENSE). Model weights không được commit vào repository.

Commercial use đối với Fish Audio materials hoặc derivative works cần separate written license từ Fish Audio theo retained license terms.

## Phạm vi release

Stable release là **v1.0.0**. Release đại diện cho các Kaggle T4x2 configurations đã được ghi tài liệu, retained evidence, reproducibility checks và repository governance mô tả ở trên.

Xem [PROJECT-CONTRACT.md](PROJECT-CONTRACT.md) để biết baseline đã khóa và acceptance criteria, cùng [final release readiness](docs/final-release-readiness.md) cho release audit.
