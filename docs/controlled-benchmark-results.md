# Controlled Benchmark Results

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](controlled-benchmark-results.vi.md)

Status: **PASS**

## Baseline
- Precision: FP16
- Batch size: 1
- max_seq_len: 4096
- torch.compile: OFF
- Semantic / Dual-AR: cuda:0
- Codec / decoder: cuda:1
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

## Observations
- Semantic throughput is very stable around 8.16–8.36 tokens/s across text-only and cloning cases.
- Median RTF improves as text/audio length increases: roughly 2.72 for short EN, about 2.64 for medium, and about 2.60–2.62 for long text-only cases.
- EN and VI medium/long behavior is closely matched under the same topology.
- GPU0 median allocated memory remains around 10.9 GB.
- GPU1 median allocated memory ranges from about 4.36 GB to 5.47 GB.
- No OOM occurred during the 40 measured runs.
- No clipping was observed in the measured runs.

## Session scope
- 8 scenarios
- 5 measured runs per scenario
- 40 measured runs total
- 2 warmup runs
- Total benchmark session: 1302.113 s

## Evidence
- `evidence/controlled-benchmark.log.gz`
- `results/controlled-benchmark/summary.json`
- Per-scenario JSON files and one retained WAV sample per scenario under `results/controlled-benchmark/`
- Reproduction runner: `scripts/run_controlled_benchmark.py`

## Conclusion
The FP16 dual-T4 baseline is stable across EN/VI short, medium, long text-only synthesis and same-language voice-cloning benchmark scenarios. The measured warm throughput and memory behavior are consistent across the benchmark matrix, with no OOM or clipping observed.
