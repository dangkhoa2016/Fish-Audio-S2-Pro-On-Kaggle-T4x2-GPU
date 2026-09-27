# Kết quả controlled benchmark

> 🌐 Language / Ngôn ngữ: [English](controlled-benchmark-results.md) | **Tiếng Việt**

Status: **PASS**

## Baseline

- Precision: FP16
- Batch size: 1
- `max_seq_len`: 4096
- `torch.compile`: OFF
- Semantic / Dual-AR: `cuda:0`
- Codec / decoder: `cuda:1`
- Warmups: 2
- Runs per scenario: 5

## Cold start

- Semantic model load: 83.363 s
- Codec load: 13.346 s
- Model ready: 96.709 s

## Warm benchmark results

| ID | Mode | Lang | Length | Median wall (s) | Median audio (s) | Median RTF | Median semantic tok/s | Median GPU0 GB | Median GPU1 GB |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| B01-en-short | text | EN | short | 13.194 | 4.923 | 2.720 | 8.276 | 10.892 | 4.438 |
| B02-vi-short | text | VI | short | 12.869 | 4.737 | 2.698 | 8.361 | 10.892 | 4.425 |
| B03-en-medium | text | EN | medium | 36.011 | 13.653 | 2.644 | 8.335 | 10.906 | 4.956 |
| B04-vi-medium | text | VI | medium | 35.111 | 13.189 | 2.644 | 8.308 | 10.906 | 4.928 |
| B05-en-long | text | EN | long | 58.209 | 22.245 | 2.617 | 8.297 | 10.922 | 5.467 |
| B06-vi-long | text | VI | long | 57.921 | 22.245 | 2.604 | 8.338 | 10.925 | 5.467 |
| B07-clone-en | cloning | EN | — | 12.384 | 4.505 | 2.749 | 8.217 | 10.944 | 4.412 |
| B08-clone-vi | cloning | VI | — | 10.361 | 3.715 | 2.800 | 8.156 | 10.947 | 4.365 |

## Quan sát

- Semantic throughput ổn định khoảng 8.16–8.36 tokens/s.
- Median RTF tốt dần khi text/audio dài hơn.
- EN và VI medium/long có behavior gần nhau trong cùng topology.
- GPU0 median allocated memory khoảng 10.9 GB.
- GPU1 khoảng 4.36–5.47 GB.
- Không OOM trong 40 measured runs.
- Không clipping trong measured runs.

## Session scope

- 8 scenarios
- 5 measured runs/scenario
- 40 measured runs
- 2 warmup runs
- Total benchmark session: 1302.113 s

## Evidence

- `evidence/controlled-benchmark.log.gz`
- `results/controlled-benchmark/summary.json`
- Per-scenario JSON và retained WAV sample trong `results/controlled-benchmark/`
- Runner: `scripts/run_controlled_benchmark.py`

## Kết luận

Dual-T4 FP16 baseline ổn định cho EN/VI short, medium, long text-only synthesis và same-language voice cloning benchmark. Warm throughput và memory behavior nhất quán trong matrix, không OOM hoặc clipping.
