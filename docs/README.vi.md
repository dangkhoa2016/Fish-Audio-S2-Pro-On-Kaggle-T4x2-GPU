# Hướng dẫn tài liệu

> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

Thư mục này phục vụ hai nhóm chính: reviewer cần hiểu các quyết định kỹ thuật và operator cần tái lập các kết quả qualification.

## Bắt đầu từ đây

1. [Tổng quan kỹ thuật](engineering-overview.vi.md) — system boundaries, hardware topology, runtime decisions và các operating mode.
2. [Ma trận qualification](qualification-matrix.vi.md) — đã kiểm tra gì, trên hardware nào và authority evidence nằm ở đâu.
3. [Hướng dẫn tái lập](reproducibility.vi.md) — clean-session procedure, ý nghĩa từng script và acceptance rules.
4. [Chỉ mục evidence](evidence-index.vi.md) — ánh xạ claims tới logs, JSON summaries, WAV outputs và reports.
5. [Lịch sử phát triển](development-history.vi.md) — engineering narrative theo thời gian và các corrective discoveries chính.

## Tài liệu chuyên sâu

- [Kiến trúc](architecture.vi.md)
- [Phương pháp benchmark](benchmark-methodology.vi.md)
- [Qualification tổng hợp song ngữ EN/VI](bilingual-text-synthesis.vi.md)
- [Qualification voice cloning kỹ thuật](technical-voice-cloning.vi.md)
- [Qualification Local HTTP API](local-api-qualification.vi.md)
- [Kết quả controlled benchmark](controlled-benchmark-results.vi.md)
- [Qualification Single-T4 INT8](single-t4-int8.vi.md)
- [Qualification Dual-Instance Concurrency](dual-instance-concurrency.vi.md)
- [Audit Release / Productization](release-productization-audit.vi.md)
- [Fresh Kaggle T4x2 Clean-Room Regression](cleanroom-regression.vi.md)
- [Synthetic multi-speaker voice-cloning acceptance](synthetic-multispeaker-voice-cloning-acceptance.vi.md)
- [Final release readiness](final-release-readiness.vi.md)
- [Xử lý sự cố](troubleshooting.vi.md)

## Authority rule

Human-readable documentation giải thích kết quả; machine-readable JSON trong `results/` và retained logs trong `evidence/` là authority artifacts cho các measured claims.

## Governance

- [Contributing](../CONTRIBUTING.md)
- [Security policy](../SECURITY.md)
- [Citation metadata](../CITATION.cff)
- [Changelog](../CHANGELOG.md)

Chạy `make audit` cho lightweight local repository audit tương ứng với CI.
