# Dual-Instance Concurrency Qualification

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](dual-instance-concurrency.vi.md)

Status: **PASS**

## Objective

Verify that the qualified single-T4 INT8 configuration can be replicated independently on both Kaggle Tesla T4 GPUs and serve two requests concurrently.

This configuration is separate from the official FP16 dual-GPU baseline. Each GPU runs a complete self-contained inference instance:
- semantic / Dual-AR: weight-only INT8;
- codec / decoder: FP16;
- batch size: 1;
- `max_seq_len=4096`;
- `torch.compile=OFF`.

## Runtime topology

- GPU0 -> instance A -> local API port 8091
- GPU1 -> instance B -> local API port 8092
- each process sees only one physical GPU through `CUDA_VISIBLE_DEVICES`
- inside each process both semantic and decoder devices are `cuda:0`

Both servers returned HTTP 200 from `/v1/health`.

## Reproduction

Build the single-T4 INT8 checkpoint first, then start one isolated API process per physical GPU.

Terminal A:

```bash
CUDA_VISIBLE_DEVICES=0 \
LISTEN=127.0.0.1:8091 \
scripts/run_api_server_single_t4_int8.sh
```

Terminal B:

```bash
CUDA_VISIBLE_DEVICES=1 \
LISTEN=127.0.0.1:8092 \
scripts/run_api_server_single_t4_int8.sh
```

Each process sees one physical T4 and therefore uses its local `cuda:0` for both semantic and codec components.

## Short-request results

| Mode | Instance A | Instance B | Effective wall time |
|---|---:|---:|---:|
| Single request | 18.412 s | 17.708 s | — |
| Concurrent pair | 18.697 s | 17.521 s | 18.697 s |

Using the measured single-request times, two sequential requests would require about 36.120 s. The concurrent two-GPU run completed both requests in 18.697 s.

Aggregate throughput improvement:

```text
36.120 / 18.697 = 1.932x
```

Measured aggregate request rate for the concurrent short pair was about 0.107 requests/s.

The concurrent latency stayed close to the single-instance latency, showing that the two independent GPU instances do not materially interfere with one another for this workload.

## Long concurrent request

- instance A: 76.984 s
- instance B: 73.729 s
- pair wall time: 76.984 s

## Memory and output validation

Peak monitored VRAM:
- GPU0: 11,092.875 MiB
- GPU1: 11,092.875 MiB

Short outputs:
- 44.1 kHz, mono
- 2.925714 s
- 258,092 bytes
- identical deterministic SHA-256 across A/B and single/concurrent runs

Long outputs:
- 44.1 kHz, mono
- 11.842177 s
- 1,044,524 bytes
- identical deterministic SHA-256 across A/B

## Evidence

- `evidence/dual-instance-concurrency/api-a-int8.log`
- `evidence/dual-instance-concurrency/api-b-int8.log`
- `evidence/dual-instance-concurrency/concurrent-vram.csv`
- `results/dual-instance-concurrency/summary.json`
- retained single, parallel, and long WAV outputs under `results/dual-instance-concurrency/`

## Conclusion

This qualification demonstrates that Kaggle T4x2 can run two independent Fish Audio S2 Pro INT8 full-pipeline instances simultaneously. For the measured short case, aggregate throughput is about 1.93x the sequential single-instance baseline while per-request latency remains nearly unchanged.

The FP16 dual-GPU configuration remains the higher-throughput semantic baseline; the INT8 path is valuable when independent concurrency and one-model-per-T4 deployment are preferred.
