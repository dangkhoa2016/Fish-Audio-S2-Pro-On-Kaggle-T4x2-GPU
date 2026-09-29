# Release / Productization Audit

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](release-productization-audit.vi.md)

Status: **PASS after corrective changes**

## Scope

This audit covers the repository for release-facing reproducibility, documentation consistency, retained evidence, licensing notes, executable scripts, secret hygiene, and alignment between public claims and measured benchmark and concurrency results.

## Findings corrected

- Fresh-session bootstrap now clones/fetches and checks out the exact Fish Speech commit in `references/upstream.lock`.
- A canonical `scripts/run_api_server_single_t4_int8.sh` runner now exists for the one-model-per-T4 topology.
- The concurrency document records the exact two-process launch commands for GPU0/8091 and GPU1/8092.
- README EN/VI reproduction guidance includes bootstrap and the concurrency runner.
- Stale notebook and dependency-placeholder wording was replaced with the current CLI-first clean-room policy.
- The pinned upstream Fish Audio Research License is retained under `THIRD_PARTY_LICENSES/`, with `NOTICE.txt` and expanded `LICENSE-NOTES.md`.

## Audit checks

- README EN/VI qualification status: consistent.
- Referenced repository paths and Markdown links: present / no broken internal links found.
- Duplicate experimental single-T4 INT8 script/doc names: absent.
- Shell runner executable bits: correct.
- Tracked model-weight files: none.
- Tracked files larger than 5 MB: none.
- Secret heuristic scan: PASS.
- Single-T4 INT8 and dual-instance concurrency summary JSON validation: PASS.
- Python script compilation: PASS.
- Shell syntax validation: PASS.
- Controlled benchmark claims match the retained report.
- Single-T4 INT8 throughput, memory, WAV metadata, and limitations match retained JSON/docs.
- Dual-instance concurrency timings, ~1.93x aggregate scaling, VRAM, and WAV metadata match retained JSON/docs.
- No subjective INT8-vs-FP16 audio-equivalence claim is made.

## Release boundaries retained

The official performance baseline remains the FP16 dual-GPU split topology. The single-T4 INT8 and dual independent-instance modes remain qualified capacity/concurrency alternatives, not replacements for that baseline.

At the time of this audit, real-human review was still listed as pending. The later release policy superseded that requirement with the reproducible synthetic multi-speaker gate; the later clean-room regression also passed.

## Next gate

The clean-room regression must run from a brand-new Kaggle T4x2 session and reproduce:

1. pinned upstream bootstrap and runtime setup;
2. FP16 dual-GPU EN/VI inference and local API;
3. single-T4 INT8 checkpoint build and single-T4 EN/VI full TTS;
4. two independent single-T4 API instances and a concurrent request pair;
5. output validation, memory checks, and no-OOM confirmation.

Do not create `v1.0.0` until the required final gates pass.
