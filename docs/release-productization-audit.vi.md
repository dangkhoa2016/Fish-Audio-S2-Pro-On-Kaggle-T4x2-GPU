# Audit Release / Productization

> 🌐 Language / Ngôn ngữ: [English](release-productization-audit.md) | **Tiếng Việt**

Status: **PASS sau corrective changes**

## Phạm vi

Audit này kiểm tra release-facing reproducibility, documentation consistency, retained evidence, licensing notes, executable scripts, secret hygiene và alignment giữa public claims với measured benchmark/concurrency results.

## Các finding đã được sửa

- Fresh-session bootstrap clone/fetch và checkout exact Fish Speech commit trong `references/upstream.lock`.
- Có canonical `scripts/run_api_server_single_t4_int8.sh` cho one-model-per-T4 topology.
- Concurrency documentation ghi exact two-process launch commands cho GPU0/8091 và GPU1/8092.
- README EN/VI reproduction guidance dùng bootstrap và canonical runners.
- Stale notebook/dependency-placeholder wording được thay bằng CLI-first clean-room policy.
- Pinned upstream Fish Audio Research License được giữ dưới `THIRD_PARTY_LICENSES/`, cùng `NOTICE.txt` và `LICENSE-NOTES.md`.

## Audit checks

- README EN/VI qualification status: consistent.
- Referenced repository paths và Markdown links: present / không broken internal links.
- Duplicate experimental single-T4 INT8 script/doc names: absent.
- Shell runner executable bits: correct.
- Tracked model-weight files: none.
- Tracked files >5 MB: none.
- Secret heuristic scan: PASS.
- Single-T4 INT8 và dual-instance concurrency summary JSON validation: PASS.
- Python script compilation: PASS.
- Shell syntax validation: PASS.
- Controlled benchmark claims match retained report.
- Single-T4 INT8 throughput, memory, WAV metadata và limitations match retained JSON/docs.
- Dual-instance concurrency timings, ~1.93x aggregate scaling, VRAM và WAV metadata match retained JSON/docs.
- Không có subjective INT8-vs-FP16 audio-equivalence claim.

## Release boundaries

Official performance baseline vẫn là FP16 dual-GPU split topology. Single-T4 INT8 và dual independent-instance modes là capacity/concurrency alternatives đã qualification, không phải replacement.

Real-human review từng được liệt kê là pending nhưng release policy sau đó supersede bằng reproducible synthetic multi-speaker gate. Clean-room regression cũng PASS.

## Final clean-room gate

Fresh Kaggle T4x2 session phải reproduce:

1. pinned upstream bootstrap và runtime setup;
2. FP16 dual-GPU EN/VI inference và local API;
3. single-T4 INT8 checkpoint build và EN/VI full TTS;
4. hai independent single-T4 API instances và concurrent request pair;
5. output validation, memory checks và no-OOM confirmation.

Không tạo `v1.0.0` cho tới khi required final gates PASS.
