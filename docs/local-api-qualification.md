# Local HTTP API Qualification

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](local-api-qualification.vi.md)

Status: **PASS for API**  
WebUI status: **not built / not required for this local API qualification**

## Runtime
- Listen: `127.0.0.1:8080` only
- Workers: 1
- Precision: FP16
- torch.compile: OFF
- Semantic device: `cuda:0`
- Decoder / reference encoder device: `cuda:1`
- max_seq_len: 4096
- max text length: 500

## API dual-GPU changes
The upstream API assumed one shared device. The project patch adds:
- `--decoder-device`
- `--max-seq-len`
- separate semantic and decoder device handling
- FP16 decoder placement
- reference audio encoding with decoder dtype
- explicit VQ code transfer to the decoder device before decode

Final cumulative patch:
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
| Streaming with non-WAV format | 400 | PASS |
| GET /ui | 404 | Expected: Awesome WebUI not built |

## Output validation
- `text-en.wav`: 44.1 kHz, 3.947 s, SHA-256 `3f8c4571b25d2ddfbbad70698f7ceddaab682fb7830b191ba98a28600c24bc5f`
- `text-vi.wav`: 44.1 kHz, 5.433 s, SHA-256 `5e8b10fb457d071ef498facc222aae2a427f5977e60c1b712be66f6c50fc1ce9`
- `reference-en.wav`: 44.1 kHz, 5.480 s, SHA-256 `a4bad2ee30b7ea86b7c92d31351632c80ecc4f30560a702c2c5544bdea32f6ef`

## Important bug found during local API qualification
The first API warmup reached semantic generation but failed when decoder weights were on `cuda:1` and generated VQ codes remained on `cuda:0`. The failure was:

`RuntimeError: Expected all tensors to be on the same device ... index is on cuda:0 ... tensors on cuda:1`

The fix explicitly transfers VQ codes to `decoder_model.device` before decoding. The server then warmed up successfully and all API acceptance tests passed.

## Evidence
- `evidence/local-api-server.log`
- `results/local-api/`
- `scripts/run_api_server_dual_gpu.sh`

## Conclusion
The Fish Audio S2 Pro local HTTP API is functional on Kaggle T4x2 with the split-device FP16 topology. Public exposure and WebUI are intentionally outside this qualification run.
