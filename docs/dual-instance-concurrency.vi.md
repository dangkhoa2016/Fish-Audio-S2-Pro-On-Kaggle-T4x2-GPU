# Qualification Dual-Instance Concurrency

> 🌐 Language / Ngôn ngữ: [English](dual-instance-concurrency.md) | **Tiếng Việt**

Status: **PASS**

## Mục tiêu

Xác minh qualified single-T4 INT8 configuration có thể được replicate độc lập trên cả hai Tesla T4 của Kaggle và phục vụ hai requests đồng thời.

Mỗi GPU chạy một complete self-contained inference instance:

- semantic / Dual-AR: weight-only INT8
- codec / decoder: FP16
- batch size: 1
- `max_seq_len=4096`
- `torch.compile=OFF`

## Runtime topology

- GPU0 -> instance A -> local API port 8091
- GPU1 -> instance B -> local API port 8092
- mỗi process chỉ nhìn thấy một GPU vật lý qua `CUDA_VISIBLE_DEVICES`
- bên trong mỗi process semantic và decoder đều dùng local `cuda:0`

Cả hai servers trả HTTP 200 từ `/v1/health`.

## Tái lập

Tạo single-T4 INT8 checkpoint trước, sau đó chạy một API process độc lập trên mỗi GPU.

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

## Short-request results

| Mode | Instance A | Instance B | Effective wall time |
|---|---:|---:|---:|
| Single request | 18.412 s | 17.708 s | — |
| Concurrent pair | 18.697 s | 17.521 s | 18.697 s |

Hai sequential requests cần khoảng 36.120 s. Concurrent T4x2 run hoàn thành cả hai trong 18.697 s.

```text
36.120 / 18.697 = 1.932x
```

Measured aggregate request rate khoảng 0.107 requests/s. Concurrent latency vẫn gần single-instance latency, cho thấy hai isolated GPU instances không materially interfere với nhau trong workload này.

## Long concurrent request

- instance A: 76.984 s
- instance B: 73.729 s
- pair wall time: 76.984 s

## Memory và output validation

Peak monitored VRAM:

- GPU0: 11,092.875 MiB
- GPU1: 11,092.875 MiB

Short outputs:

- 44.1 kHz, mono
- 2.925714 s
- 258,092 bytes
- deterministic SHA-256 giống nhau giữa A/B và single/concurrent runs

Long outputs:

- 44.1 kHz, mono
- 11.842177 s
- 1,044,524 bytes
- deterministic SHA-256 giống nhau giữa A/B

## Evidence

- `evidence/dual-instance-concurrency/api-a-int8.log`
- `evidence/dual-instance-concurrency/api-b-int8.log`
- `evidence/dual-instance-concurrency/concurrent-vram.csv`
- `results/dual-instance-concurrency/summary.json`
- retained single, parallel và long WAV trong `results/dual-instance-concurrency/`

## Kết luận

Kaggle T4x2 chạy đồng thời được hai independent Fish Audio S2 Pro INT8 full-pipeline instances. Với short case đã đo, aggregate throughput khoảng 1.93x sequential baseline trong khi per-request latency gần như giữ nguyên.

Dual-T4 FP16 vẫn là semantic performance baseline nhanh hơn; INT8 phù hợp khi ưu tiên independent concurrency và one-model-per-T4 deployment.
