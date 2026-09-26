# Technical Voice-Cloning Qualification

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](technical-voice-cloning.vi.md)

Status: **PASS (technical qualification)**

## Scope
This run validates the Fish Audio S2 Pro voice-cloning execution path on Kaggle T4x2 using synthetic reference WAVs produced by the already-qualified bilingual text-synthesis qualification pipeline.

This was an early technical synthetic-reference qualification. The current release qualification has since been superseded by the reproducible 8-speaker synthetic multi-speaker gate documented in `docs/synthetic-multispeaker-voice-cloning-acceptance.md`.

## References
- EN reference: `results/bilingual-text-synthesis/T03-en-medium.wav`
- VI reference: `results/bilingual-text-synthesis/T04-vi-medium.wav`
- Both references: 44.1 kHz mono, about 14.814 s
- Both encoded successfully to VQ shape `[10, 319]`

## Runtime topology
- Semantic / Dual-AR: `cuda:0`
- Codec / reference encoder / decoder: `cuda:1`
- Precision: FP16
- max_seq_len: 4096
- torch.compile: OFF

## Test matrix
| ID | Reference | Target | Duration (s) | RTF | Clipping |
|---|---|---|---:|---:|---:|
| C01-en-to-en | EN | EN | 8.266 | 2.693 | 0.000 |
| C02-en-to-vi | EN | VI | 8.266 | 2.639 | 0.000 |
| C03-vi-to-vi | VI | VI | 7.941 | 2.744 | 0.000 |
| C04-vi-to-en | VI | EN | 7.570 | 2.691 | 0.000 |

## Aggregate
- Cases passed: 4 / 4
- Mean RTF: 2.692
- Max GPU0 allocated: 10.949 GB
- Max GPU1 allocated: 4.636 GB
- All WAV outputs valid
- Clipping ratio: 0 for all four outputs
- No OOM
- No device mismatch

## Evidence
- `evidence/technical-voice-cloning.log.gz`
- `results/technical-voice-cloning/summary.json`
- Per-case JSON + WAV files in `results/technical-voice-cloning/`

## Conclusion
The voice-cloning path is technically functional on the dual-T4 FP16 topology for same-language and cross-language generation.

The original plan for a mandatory real-human gate was later superseded. Real-human references remain an optional private extension, not a release blocker.
