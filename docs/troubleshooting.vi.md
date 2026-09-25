# Xử lý sự cố

> 🌐 Language / Ngôn ngữ: [English](troubleshooting.md) | **Tiếng Việt**

## Single T4 OOM

Nếu full FP16 trên T4 16 GB tái lập OOM ổn định với upstream configuration đã kiểm tra, hãy xem đó là một kết quả characterization dự kiến. Không nên lặp lại cùng một cấu hình không kiểm soát chỉ để tiêu tốn thêm GPU quota.

## Device mismatch

Log device và dtype của từng component đã load. Semantic codes phải được chuyển tường minh sang decoder device trước decode.

## Kaggle package drift

Sau GPU PASS đầu tiên, ghi lại Python, PyTorch, CUDA, driver và `pip freeze`, sau đó pin môi trường đang hoạt động.

## Compile problems

Giữ `torch.compile` ở trạng thái disabled cho tới khi correctness baseline PASS.
