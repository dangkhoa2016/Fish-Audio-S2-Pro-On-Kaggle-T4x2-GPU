# Hướng dẫn tái lập

> 🌐 Language / Ngôn ngữ: [English](reproducibility.md) | **Tiếng Việt**

Tài liệu này là operational entry point để tái lập các Fish Audio S2 Pro paths đã qualification từ một Kaggle session mới. Mục tiêu không chỉ là liệt kê lệnh chạy mà còn giải thích vì sao từng file tồn tại, nó thuộc operating path nào và evidence nào phải được tạo ra.

## Môi trường bắt buộc

- Kaggle notebook với GPU accelerator **T4 x2** cho dual-GPU và concurrency paths.
- Fish Audio S2 Pro Kaggle model attachment.
- VoxCPM2 Kaggle model attachment khi tái lập independent synthetic multi-speaker acceptance.
- Internet access trong bootstrap nếu cần tải dependency hoặc pinned upstream source.
- Clean checkout của repository này.

Single-T4 INT8 path dùng một Tesla T4 tại một thời điểm. Dual-T4 FP16 và two-instance concurrency cần cả hai GPU.

## Reproducibility contract

Một reproduction chỉ hợp lệ khi bắt đầu từ clean checkout và dùng đúng Fish Speech revision trong `references/upstream.lock`.

Không thay bằng arbitrary newer upstream commit rồi xem kết quả là tương đương release đã qualification. Model weights nằm ngoài Git và được mount từ Kaggle.

## Các khu vực repository dùng trong reproduction

| Path | Mục đích |
|---|---|
| `scripts/` | setup, inference, qualification, benchmark, verification và reporting entry points |
| `patches/` | repository-owned changes áp dụng lên pinned Fish Speech checkout |
| `references/` | source/model provenance, upstream pin và synthetic-reference records |
| `results/` | machine-readable summaries và retained result artifacts |
| `evidence/` | runtime logs và supporting execution evidence |
| `reports/` | reviewer-facing generated reports |
| `docs/` | architecture, methodology, qualification và release documentation |

## Core bootstrap sequence

```bash
./scripts/bootstrap_kaggle.sh
./scripts/preflight.sh
./scripts/setup_runtime.sh
./scripts/apply_upstream_patch.sh
```

### `scripts/bootstrap_kaggle.sh`

**Mục đích:** tạo canonical working environment từ fresh Kaggle session.

Script checkout exact Fish Speech revision từ `references/upstream.lock`, chuẩn bị layout và phát hiện attached Fish Audio S2 Pro model.

**Dùng khi:** bắt đầu bất kỳ clean reproduction nào.

**Expected result:** pinned upstream source và model paths sẵn sàng.

### `scripts/preflight.sh`

**Mục đích:** reject môi trường không hỗ trợ hoặc thiếu thành phần trước expensive model loading.

**Dùng khi:** ngay sau bootstrap.

**Expected result:** T4/T4x2 topology cần thiết được xác nhận hoặc fail sớm với lỗi rõ ràng.

### `scripts/setup_runtime.sh`

**Mục đích:** cài và chuẩn bị Python/runtime dependencies cho pinned Fish Speech source và repository runners.

### `scripts/inventory_model.py`

**Mục đích:** inventory attached S2 Pro model payload để xác nhận model attachment/provenance.

### `scripts/apply_upstream_patch.sh`

**Mục đích:** apply repository-owned compatibility/runtime patches vào exact pinned Fish Speech checkout.

## Dual-T4 FP16 path

### `scripts/run_dual_gpu_fp16.sh`

Canonical dual-T4 FP16 CLI synthesis runner. GPU0 host Dual-AR/text-to-semantic + KV cache; GPU1 host codec/reference/audio decoder.

**Acceptance:** phải tạo WAV non-empty và runtime logs; process exit 0 nhưng thiếu WAV không được xem là PASS.

### `scripts/qualify_text_synthesis.py`

Qualification English/Vietnamese text-only synthesis trên retained bilingual matrix.

**Outputs:** structured results, retained WAVs và evidence tương ứng với `docs/bilingual-text-synthesis.md`.

### `scripts/qualify_voice_cloning.py`

Reproduce technical synthetic-reference voice-cloning matrix ban đầu.

Đây là technical milestone; final speaker-cloning authority dùng independent VoxCPM2 reference bank.

### `scripts/run_api_server_dual_gpu.sh`

Launch qualified local HTTP API trên dual-T4 FP16 topology. Health, text synthesis, reference handling, cloning và documented rejection paths phải match `docs/local-api-qualification.md`.

## Controlled benchmark

### `scripts/run_controlled_benchmark.py`

Chạy controlled FP16 benchmark với batch 1, `max_seq_len=4096`, compile OFF, 2 warmups, 8 scenarios và 5 measured runs/scenario.

**Authority:** `docs/benchmark-methodology.md`, `docs/controlled-benchmark-results.md`, `results/controlled-benchmark/`, `evidence/controlled-benchmark.log.gz`.

## Single-T4 INT8 path

### `scripts/quantize_single_t4_int8.py`

Tạo weight-only INT8 semantic checkpoint. Codec vẫn FP16. Đây là capacity optimization, không phải speed optimization.

### `scripts/run_single_t4_int8.sh`

Chạy complete TTS trên một T4 với INT8 semantic + FP16 codec.

**Acceptance:** output WAV non-empty, memory và semantic throughput phù hợp documented profile.

### `scripts/run_api_server_single_t4_int8.sh`

Expose single-T4 INT8 path qua local API, dùng cho isolated instance trong concurrency design.

## Hai T4 instance độc lập

Dual-instance mode chạy một complete INT8 API process trên GPU0 và một trên GPU1. Đây là hai services độc lập, không phải model sharding qua pooled 32 GB VRAM.

Exact launch/measurement commands nằm tại `docs/dual-instance-concurrency.md`. Clean-room authority reproduce khoảng `2.0126x` aggregate scaling cho deterministic request đã kiểm tra.

## Independent synthetic multi-speaker path

Final voice-cloning gate dùng references từ model khác để tránh self-reference vòng tròn.

### `scripts/setup_voxcpm2_reference_runtime.sh`

Chuẩn bị VoxCPM2 runtime dùng riêng cho synthetic reference generation.

### `scripts/generate_synthetic_speaker_bank.py`

Tạo 8-speaker bank: 4 English + 4 Vietnamese với vocal profiles khác nhau.

**Output:** reference WAV bank và `results/synthetic-speaker-bank/summary.json`.

### `scripts/qualify_synthetic_multispeaker.py`

Chạy S2 Pro cloning với independent bank: 8 same-language + 4 cross-language cases.

**Output:** 12 clone outputs và `results/synthetic-multispeaker-acceptance/summary.json`.

### `scripts/score_synthetic_speakers.py`

Independent speaker discrimination bằng WavLM-based speaker encoder.

**Acceptance rule:** mỗi clone so với cả 8 references; intended speaker phải top-1.

**Qualified result:** 12/12 top-1.

### `scripts/check_synthetic_repeatability.py`

Kiểm tra deterministic repeatability.

**Acceptance:** regenerated outputs phải byte-identical.

**Qualified result:** 2/2 byte-identical.

### `scripts/build_synthetic_review_html.py`

Tạo `reports/synthetic-multispeaker-review.html` để nghe side-by-side. Human listening chỉ là optional spot-check, không phải machine-readable release gate.

## Tổ chức results và evidence

- `results/`: structured authority summaries.
- `evidence/`: runtime logs và supporting evidence.
- `reports/`: reviewer-facing generated material.
- `docs/`: capability-specific methodology và interpretation.

Narrative documentation không được override machine-readable authority artifact trái ngược.

## Acceptance discipline

- Không runner nào được báo PASS nếu expected output thiếu hoặc empty.
- Audio-producing path phải có WAV thực sự chứa data.
- Runtime metrics, hashes và metadata phải được capture trước conclusions.
- Secrets và model weights không vào Git.
- Clean-room failure override development-session success cho tới khi defect được sửa.
- Không suy rộng tested behavior sang hardware/settings/speakers/workloads chưa kiểm tra.

## Repository verification

```bash
make audit
```

Audit kiểm tra shell syntax, Python compilation, JSON validity, internal Markdown links, model-weight policy, whitespace và common secret patterns. GPU qualification tách riêng vì CI không cung cấp Kaggle T4x2 baseline.

## Tài liệu liên quan

- [Tổng quan kỹ thuật](engineering-overview.vi.md)
- [Ma trận qualification](qualification-matrix.vi.md)
- [Chỉ mục evidence](evidence-index.vi.md)
- [Kiến trúc](architecture.vi.md)
- [Phương pháp benchmark](benchmark-methodology.vi.md)
- [Xử lý sự cố](troubleshooting.vi.md)
- [Final release readiness](final-release-readiness.vi.md)
