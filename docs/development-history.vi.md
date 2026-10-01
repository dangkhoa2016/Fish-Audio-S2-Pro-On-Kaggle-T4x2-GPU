# Lịch sử phát triển

> 🌐 Language / Ngôn ngữ: [English](development-history.md) | **Tiếng Việt**

## 1. Thiết lập reproducible baseline

Dự án bắt đầu bằng việc pin Fish Speech runtime, inventory model S2 Pro được mount từ Kaggle, định nghĩa hardware contract T4x2 và tách repository artifacts khỏi model weights.

## 2. Characterize memory boundary

Single-T4 semantic generation thành công, trong khi full FP16 TTS vượt quá practical memory envelope của một T4. Kết quả này xác lập nhu cầu explicit component placement thay vì xem hai GPU như pooled memory.

## 3. Qualification dual-T4 FP16 topology

Semantic model và KV cache được đặt trên GPU0; codec/reference/decode đặt trên GPU1. English/Vietnamese text synthesis, technical synthetic-reference cloning và local HTTP API đều được validate.

## 4. Đo trước khi tối ưu

Controlled benchmark được bổ sung với fixed scenarios, warmups, repeated measurements, RTF, semantic token rate, audio duration và VRAM observations. Đây trở thành performance authority thay cho ad-hoc terminal timing.

## 5. Bổ sung single-T4 capacity path

Weight-only INT8 quantization cho semantic model giúp full TTS chạy trên một T4 trong khi codec vẫn FP16. Đây là capacity trade-off, không phải replacement cho FP16 performance baseline.

## 6. Dùng T4x2 cho concurrent capacity

Hai single-T4 INT8 API instance độc lập được qualification, mỗi GPU một process. Concurrent requests giữ per-request latency đủ gần baseline để chứng minh xấp xỉ hai lần aggregate capacity cho request đã kiểm tra.

## 7. Harden productization và licensing

Bootstrap behavior, upstream pin enforcement, canonical runners, license retention, NOTICE attribution, secret hygiene và documentation consistency được audit trước release qualification.

## 8. Reproduce từ một Kaggle session mới

Clean-room run tìm ra các defect bị che bởi development session dài: cumulative patch application, relative output path sau khi đổi directory và false PASS khi WAV bị thiếu. Các defect này được sửa và toàn bộ stack được re-qualified.

## 9. Thay thế final gate khó tái lập

Mandatory real-human voice gate từng được cân nhắc nhưng không được dùng làm release authority vì privacy, consent và repeatability constraints. Nó được thay bằng independent VoxCPM2 synthetic speaker bank: bốn English và bốn Vietnamese speakers, same-language/cross-language cloning, WavLM speaker discrimination độc lập, deterministic repeats và listening report.

## 10. Release qualification

Final audit reconcile machine-readable fields, validate repository hygiene, giữ license/evidence chain và khóa release baseline v1.0.0.

## Bài học kỹ thuật

Dự án không chỉ chứng minh S2 Pro chạy được trên Kaggle T4x2. Repository còn ghi lại cách constraints được đo, assumption sai làm thay đổi design ra sao, clean-room testing phát hiện reproducibility defect như thế nào và vì sao release claims chỉ được giới hạn trong evidence thực sự hỗ trợ.
