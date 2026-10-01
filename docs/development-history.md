# Development History

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](development-history.vi.md)

## 1. Establish the reproducible baseline

The project began by pinning the Fish Speech runtime, inventorying the Kaggle-mounted S2 Pro model, defining the T4x2 hardware contract, and separating repository artifacts from model weights.

## 2. Characterize the memory boundary

Single-T4 semantic generation succeeded, while full FP16 TTS exceeded a single T4's practical memory envelope. That result established the need for explicit component placement rather than treating two GPUs as pooled memory.

## 3. Qualify the dual-T4 FP16 topology

The semantic model and KV cache were placed on GPU0 while codec/reference/decode work was placed on GPU1. English and Vietnamese text synthesis, synthetic-reference cloning, and a local HTTP API were validated.

## 4. Measure before optimizing

A controlled benchmark was added with fixed scenarios, warmups, repeated measurements, RTF, semantic token rate, audio duration, and VRAM observations. This became the performance authority rather than ad-hoc terminal timings.

## 5. Add a single-T4 capacity path

Weight-only INT8 quantization of the semantic model enabled full TTS on one T4 while retaining the FP16 codec. The result was treated as a capacity trade-off, not as a replacement for the FP16 performance baseline.

## 6. Use T4x2 for concurrent capacity

Two isolated single-T4 INT8 API instances were qualified, one per physical GPU. Concurrent requests preserved per-request latency closely enough to demonstrate approximately twofold aggregate capacity for the tested request.

## 7. Harden productization and licensing

Bootstrap behavior, upstream pin enforcement, canonical runners, license retention, NOTICE attribution, secret hygiene, and documentation consistency were audited before release qualification.

## 8. Reproduce from a fresh Kaggle session

The clean-room run found defects that development sessions had hidden: cumulative patch application, relative output paths after changing directories, and false PASS reporting when a WAV was missing. Those defects were corrected and the complete stack was re-qualified.

## 9. Replace an unreproducible final gate

A mandatory real-human voice gate was considered but rejected as the release authority because it introduced privacy, consent, and repeatability constraints. It was replaced by an independent VoxCPM2 synthetic speaker bank: four English and four Vietnamese speakers, same-language and cross-language cloning, independent WavLM speaker discrimination, deterministic repeats, and a listening report.

## 10. Release qualification

The final audit reconciled historical machine-readable fields, validated repository hygiene, retained the license and evidence chain, and locked the v1.0.0 release baseline.

## Engineering lesson

The project is not only a demonstration that S2 Pro can run on Kaggle T4x2. The repository records how constraints were measured, how failed assumptions changed the design, how clean-room testing discovered reproducibility defects, and how release claims were narrowed to what the retained evidence actually supports.
