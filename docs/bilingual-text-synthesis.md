# Bilingual Text-Synthesis Qualification

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](bilingual-text-synthesis.vi.md)

Status: **PASS — technical generation only; native Vietnamese pronunciation not qualified**

## Runtime
- Semantic device: `cuda:0` / Tesla T4
- Decoder device: `cuda:1` / Tesla T4
- Precision: FP16
- max_seq_len: 4096
- torch.compile: OFF
- Semantic model load: 81.285 s
- Codec load: 13.102 s

## Test matrix
| ID | Language | Category | Audio duration (s) | Inference (s) | RTF | Clipping |
|---|---|---|---:|---:|---:|---:|
| T01-en-short | EN | short | 5.155 | 15.753 | 3.056 | 0.000 |
| T02-vi-short | VI | short | 5.805 | 15.537 | 2.677 | 0.000 |
| T03-en-medium | EN | medium | 14.814 | 38.758 | 2.616 | 0.000 |
| T04-vi-medium | VI | medium | 14.814 | 38.569 | 2.603 | 0.000 |
| T05-en-expressive | EN | expressive | 12.214 | 32.030 | 2.622 | 0.000 |
| T06-vi-expressive | VI | expressive | 11.842 | 31.188 | 2.634 | 0.000 |

## Aggregate
- Cases passed: 6 / 6
- Mean RTF: 2.701
- RTF range: 2.603–3.056
- Max GPU0 allocated memory: 10.912 GB
- Max GPU1 allocated memory: 5.027 GB
- All outputs: WAV, mono, 44.1 kHz, PCM16
- Clipping ratio: 0 for all six cases

## Evidence
- `evidence/bilingual-text-synthesis.log.gz`
- `results/bilingual-text-synthesis/summary.json`
- Per-case JSON and WAV files under `results/bilingual-text-synthesis/`

## Conclusion
The dual-GPU FP16 baseline passed the English/Vietnamese **technical generation** matrix across short, medium, and expressive prompts without OOM. PASS here means successful generation of structurally valid audio under the documented runtime checks. It does not qualify native Vietnamese accent, pronunciation, or tonal naturalness. Human listening in the final pre-public notebook review found Vietnamese noticeably non-native, including after same-language VoxCPM2 conditioning; native Vietnamese pronunciation is therefore NOT QUALIFIED in v1.0.0.
