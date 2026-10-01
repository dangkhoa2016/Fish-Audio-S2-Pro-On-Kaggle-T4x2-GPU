# Notebooks

> 🌐 Language / Ngôn ngữ: **English + Tiếng Việt in the same notebook**

## Kaggle production demo

The canonical interactive entry point is:

- [`kaggle-production-demo.ipynb`](kaggle-production-demo.ipynb)

### English

Use a **fresh Kaggle Notebook**, select **GPU T4 ×2**, enable **Internet**, then use **Add Input → Models** to attach:

`dangkhoa2016/fishaudio-s2-pro` — **PyTorch / default / version 1**

Expected read-only mount:

`/kaggle/input/models/dangkhoa2016/fishaudio-s2-pro/pytorch/default/1`

No external Kaggle Dataset is required for the default production demo.

The notebook is presentation-oriented but thin: it explains every execution phase in English and Vietnamese, while the actual runtime work is delegated to the repository's canonical scripts. The showcase includes bilingual FP16 synthesis, reviewer-facing audio playback and metrics, synthetic-reference cross-language voice cloning, local HTTP API TTS, and a final machine-readable scorecard.

For publication-quality evidence, use **Restart Session → Run All** exactly once on a fresh T4×2 session.

The canonical notebook completed this clean fresh-session acceptance on 2026-10-01. The retained scorecard reports **6 / 6 bilingual cases**, **4 / 4 voice-cloning cases**, successful local API health + EN/VI TTS, and `KAGGLE_PRODUCTION_DEMO=PASS`. See `../evidence/kaggle-production-demo.log` and `../results/notebook-production-demo/production-demo-summary.json`.

### Tiếng Việt

Hãy dùng một **fresh Kaggle Notebook**, chọn **GPU T4 ×2**, bật **Internet**, rồi dùng **Add Input → Models** để attach:

`dangkhoa2016/fishaudio-s2-pro` — **PyTorch / default / version 1**

Mount read-only dự kiến:

`/kaggle/input/models/dangkhoa2016/fishaudio-s2-pro/pytorch/default/1`

Default production demo **không cần attach Kaggle Dataset ngoài**.

Notebook tập trung mạnh vào presentation nhưng vẫn giữ code surface mỏng: mỗi phase chạy đều có phần giải thích English + Vietnamese, còn runtime thật được giao cho canonical scripts của repository. Showcase gồm tổng hợp giọng nói FP16 song ngữ, audio playback + metrics dễ review, synthetic-reference cross-language voice cloning, local HTTP API TTS và final machine-readable scorecard.

Để tạo publication evidence sạch, hãy dùng **Restart Session → Run All** đúng một lần trên fresh T4×2 session.

Canonical notebook đã hoàn tất clean fresh-session acceptance này vào 2026-10-01. Retained scorecard ghi nhận **6 / 6 bilingual cases**, **4 / 4 voice-cloning cases**, local API health + EN/VI TTS thành công và `KAGGLE_PRODUCTION_DEMO=PASS`. Xem `../evidence/kaggle-production-demo.log` và `../results/notebook-production-demo/production-demo-summary.json`.

> The repository CLI workflow remains the source of truth; notebook correctness must not depend on notebook-only state.
