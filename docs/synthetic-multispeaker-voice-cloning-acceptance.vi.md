# Synthetic Multi-Speaker Voice-Cloning Acceptance

> 🌐 Language / Ngôn ngữ: [English](synthetic-multispeaker-voice-cloning-acceptance.md) | **Tiếng Việt**

Status: **PASS — reproducible technical, speaker-discrimination và repeatability gates**

## Phạm vi

Final reproducible voice-cloning gate dùng independent TTS model OpenBMB VoxCPM2 để tạo synthetic speaker bank. Không cần giọng người thật.

Benchmark đánh giá speaker conditioning của Fish Audio S2 Pro trên nhiều synthetic speakers bằng English và Vietnamese. Kết quả **không** tuyên bố universal equivalence với arbitrary real-human voices.

## Reference generator

- Model: `openbmb/VoxCPM2`
- Kaggle mirror: `dangkhoa2016/openbmb-voxcpm2`
- Resolved upstream commit: `32279effe8c19989596f05d353d1447f51d9e915`
- Python package: `voxcpm==2.0.3`
- Mode: Voice Design
- Output: 48 kHz mono
- `cfg_value=2.0`
- `inference_timesteps=10`

Model card và mirror provenance xác định VoxCPM2 dùng Apache-2.0.

## Canonical speaker bank

| ID | Language | Reference duration | Clipping |
|---|---|---:|---:|
| en-f01 | EN | 14.24 s | 0 |
| en-f02 | EN | 14.72 s | 0 |
| en-m01 | EN | 13.12 s | 0 |
| en-m02 | EN | 16.00 s | 0 |
| vi-f01 | VI | 13.44 s | 0 |
| vi-f02 | VI | 14.88 s | 0 |
| vi-m01 | VI | 14.40 s | 0 |
| vi-m02 | VI | 14.24 s | 0 |

Descriptions cố ý thay đổi gender presentation, age, timbre, energy và pacing. Exact transcripts và SHA-256 nằm trong `results/synthetic-speaker-bank/summary.json`.

## S2 Pro matrix

S2 Pro chạy với accepted dual-T4 FP16 topology:

- GPU0: semantic / Dual-AR / KV cache
- GPU1: codec / reference encoder / decoder
- `max_seq_len=4096`
- `torch.compile=OFF`

Model và codec load một lần; cả 8 references encode một lần.

Acceptance cases:

- 8 same-language clones
- 4 cross-language clones:
  - `en-f01 -> VI`
  - `en-m02 -> VI`
  - `vi-f01 -> EN`
  - `vi-m02 -> EN`

Result: **12 / 12 technical cases PASS**.

Aggregate technical results:

- mean output duration: ~9.973 s
- output duration range: ~8.266–11.471 s
- mean RTF: ~2.711
- RTF range: ~2.693–2.774
- maximum clipping ratio: 0
- peak allocated GPU0: 10,948,754,944 bytes
- peak allocated GPU1: 4,826,770,944 bytes
- không OOM
- không device mismatch

## Independent speaker-discrimination evidence

Verifier:

- `microsoft/wavlm-base-plus-sv`
- pinned revision: `feb593a6c23c1cc3d9510425c29b0a14d2b07b1e`
- WavLM x-vector embeddings
- normalized cosine similarity

Mỗi S2 Pro output được so với **toàn bộ 8** VoxCPM2 references. Không dùng arbitrary absolute cosine threshold; test kiểm tra intended speaker có đứng thứ nhất trong complete reference bank hay không.

Results:

- overall top-1: **12 / 12**
- same-language top-1: **8 / 8**
- cross-language top-1: **4 / 4**
- mean intended-speaker cosine: **0.96917**
- mean margin over best impostor: **0.14344**
- minimum margin over best impostor: **0.03186**, vẫn dương

Đây là relative speaker-identification evidence, không phải absolute perceptual-quality score.

## Deterministic repeatability

Hai same-language cases đại diện được regenerate từ fresh S2 Pro model load với cùng input và seed:

- `en-f01-same`
- `vi-f01-same`

Result: **2 / 2 byte-identical**.

Cả byte count và SHA-256 đều match chính xác.

## Listening review

`reports/synthetic-multispeaker-review.html` cung cấp side-by-side players cho reference, same-language clone, selected cross-language clone và deterministic repeat.

Human listening hữu ích cho naturalness, pronunciation và obvious artifacts, nhưng không cần real-person voice.

## Tái lập

1. Attach:
   - `dangkhoa2016/fishaudio-s2-pro`
   - `dangkhoa2016/openbmb-voxcpm2`
2. Chạy `scripts/setup_voxcpm2_reference_runtime.sh`.
3. Tạo references bằng `scripts/generate_synthetic_speaker_bank.py`.
4. Bootstrap Fish Speech bằng `scripts/bootstrap_kaggle.sh`.
5. Chạy `scripts/setup_runtime.sh` và `scripts/apply_upstream_patch.sh`.
6. Chạy `scripts/qualify_synthetic_multispeaker.py`.
7. Chạy `scripts/score_synthetic_speakers.py`.
8. Chạy `scripts/check_synthetic_repeatability.py`.
9. Chạy `scripts/build_synthetic_review_html.py`.

## Authority artifacts

- `results/synthetic-speaker-bank/summary.json`
- `results/synthetic-multispeaker-acceptance/summary.json`
- `results/synthetic-multispeaker-acceptance/speaker-verification.json`
- `results/synthetic-multispeaker-repeatability/summary.json`
- `evidence/synthetic-speaker-bank.log`
- `evidence/synthetic-multispeaker-acceptance.log`
- `evidence/synthetic-speaker-verification.log`
- `evidence/synthetic-multispeaker-repeatability.log`

## Acceptance boundary

Gate này supersede mandatory real-human-reference release gate từng được dự kiến.

Optional private real-human evaluation vẫn có thể thực hiện như experiment bổ sung, nhưng không bắt buộc cho reproducible release qualification của repository.
