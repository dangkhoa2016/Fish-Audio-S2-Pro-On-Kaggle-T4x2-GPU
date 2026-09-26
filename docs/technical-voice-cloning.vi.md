# Qualification voice cloning kỹ thuật

> 🌐 Language / Ngôn ngữ: [English](technical-voice-cloning.md) | **Tiếng Việt**

Status: **PASS (technical qualification)**

## Phạm vi

Run này validate execution path voice cloning của Fish Audio S2 Pro trên Kaggle T4x2 bằng synthetic reference WAV được tạo từ bilingual text-synthesis pipeline đã qualification.

Đây là technical synthetic-reference qualification ban đầu. Release qualification hiện tại dùng reproducible 8-speaker synthetic multi-speaker gate tại `docs/synthetic-multispeaker-voice-cloning-acceptance.md`, vì vậy tài liệu này được giữ như một technical milestone chứ không phải final speaker-cloning authority.

## References

- EN reference: `results/bilingual-text-synthesis/T03-en-medium.wav`
- VI reference: `results/bilingual-text-synthesis/T04-vi-medium.wav`
- Cả hai: 44.1 kHz mono, khoảng 14.814 s
- Cả hai encode thành công tới VQ shape `[10, 319]`

## Runtime topology

- Semantic / Dual-AR: `cuda:0`
- Codec / reference encoder / decoder: `cuda:1`
- Precision: FP16
- `max_seq_len`: 4096
- `torch.compile`: OFF

## Ma trận kiểm tra

| ID | Reference | Target | Duration (s) | RTF | Clipping |
|---|---|---|---:|---:|---:|
| C01-en-to-en | EN | EN | 8.266 | 2.693 | 0.000 |
| C02-en-to-vi | EN | VI | 8.266 | 2.639 | 0.000 |
| C03-vi-to-vi | VI | VI | 7.941 | 2.744 | 0.000 |
| C04-vi-to-en | VI | EN | 7.570 | 2.691 | 0.000 |

## Tổng hợp

- Cases passed: 4 / 4
- Mean RTF: 2.692
- Max GPU0 allocated: 10.949 GB
- Max GPU1 allocated: 4.636 GB
- Tất cả WAV hợp lệ
- Clipping ratio: 0 cho cả bốn outputs
- Không OOM
- Không device mismatch

## Evidence

- `evidence/technical-voice-cloning.log.gz`
- `results/technical-voice-cloning/summary.json`
- Per-case JSON + WAV trong `results/technical-voice-cloning/`

## Kết luận

Voice-cloning path hoạt động kỹ thuật trên dual-T4 FP16 topology cho cả same-language và cross-language generation.

Mandatory real-human gate từng được cân nhắc nhưng đã được supersede. Real-human references chỉ còn là optional private extension, không phải release blocker.
