# Qualification Local HTTP API

> 🌐 Language / Ngôn ngữ: [English](local-api-qualification.md) | **Tiếng Việt**

Status: **PASS cho API**  
WebUI status: **không build / không bắt buộc trong qualification này**

## Runtime

- Listen: `127.0.0.1:8080`
- Workers: 1
- Precision: FP16
- `torch.compile`: OFF
- Semantic device: `cuda:0`
- Decoder / reference encoder: `cuda:1`
- `max_seq_len`: 4096
- max text length: 500

## Thay đổi dual-GPU cho API

Upstream API giả định một shared device. Patch của dự án bổ sung:

- `--decoder-device`
- `--max-seq-len`
- semantic và decoder device tách biệt
- FP16 decoder placement
- reference audio encoding theo decoder dtype
- explicit VQ code transfer sang decoder device trước decode

Cumulative patch:

- `patches/api-dual-gpu/0002-api-dual-gpu-cumulative.patch`
- SHA-256: `0feab8dad2e5e6f96a7d23df4ae2dd5ae5fe9869e66e1cbc70b16ce8796f16cc`

## Acceptance

| Check | HTTP | Result |
|---|---:|---|
| GET /v1/health | 200 | PASS |
| EN text-only TTS | 200 | PASS |
| VI text-only TTS | 200 | PASS |
| Add saved reference | 200 | PASS |
| List saved references | 200 | PASS |
| TTS with reference_id | 200 | PASS |
| Text > 500 chars | 400 | PASS |
| Streaming với non-WAV format | 400 | PASS |
| GET /ui | 404 | Expected: Awesome WebUI chưa build |

## Output validation

- `text-en.wav`: 44.1 kHz, 3.947 s, SHA-256 `3f8c4571b25d2ddfbbad70698f7ceddaab682fb7830b191ba98a28600c24bc5f`
- `text-vi.wav`: 44.1 kHz, 5.433 s, SHA-256 `5e8b10fb457d071ef498facc222aae2a427f5977e60c1b712be66f6c50fc1ce9`
- `reference-en.wav`: 44.1 kHz, 5.480 s, SHA-256 `a4bad2ee30b7ea86b7c92d31351632c80ecc4f30560a702c2c5544bdea32f6ef`

## Bug quan trọng được phát hiện

Warmup đầu tiên đi qua semantic generation nhưng fail khi decoder weights ở `cuda:1` còn generated VQ codes ở `cuda:0`.

Lỗi:

`RuntimeError: Expected all tensors to be on the same device ... index is on cuda:0 ... tensors on cuda:1`

Cách sửa là chuyển VQ codes tường minh sang `decoder_model.device` trước decode. Sau đó server warmup thành công và toàn bộ API acceptance tests PASS.

## Evidence

- `evidence/local-api-server.log`
- `results/local-api/`
- `scripts/run_api_server_dual_gpu.sh`

## Kết luận

Local HTTP API của Fish Audio S2 Pro hoạt động trên Kaggle T4x2 với split-device FP16 topology. Public exposure và WebUI nằm ngoài phạm vi qualification này.
