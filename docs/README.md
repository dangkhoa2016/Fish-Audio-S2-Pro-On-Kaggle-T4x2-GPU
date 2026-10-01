# Documentation Guide

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

This directory is organized for two audiences: reviewers who want to understand the engineering decisions, and operators who want to reproduce the qualification results.

## Start here

1. [Engineering overview](engineering-overview.md) — system boundaries, hardware topology, runtime decisions, and supported operating modes.
2. [Qualification matrix](qualification-matrix.md) — what was tested, on which hardware, and where the authority evidence lives.
3. [Reproducibility guide](reproducibility.md) — clean-session procedure and acceptance rules.
4. [Evidence index](evidence-index.md) — map from claims to logs, JSON summaries, WAV outputs, and reports.
5. [Development history](development-history.md) — chronological engineering narrative and major corrective discoveries.

## Deep-dive records

- [Architecture](architecture.md)
- [Benchmark methodology](benchmark-methodology.md)
- [Bilingual text-synthesis qualification](bilingual-text-synthesis.md)
- [Technical voice-cloning qualification](technical-voice-cloning.md)
- [Local HTTP API qualification](local-api-qualification.md)
- [Controlled benchmark results](controlled-benchmark-results.md)
- [Single-T4 INT8 qualification](single-t4-int8.md)
- [Dual-instance concurrency qualification](dual-instance-concurrency.md)
- [Release / productization audit](release-productization-audit.md)
- [Fresh clean-room regression](cleanroom-regression.md)
- [Synthetic multi-speaker acceptance](synthetic-multispeaker-voice-cloning-acceptance.md)
- [Final release readiness](final-release-readiness.md)
- [Troubleshooting](troubleshooting.md)

## Authority rule

Narrative documents explain the results; machine-readable JSON under `results/` and retained logs under `evidence/` are the authority artifacts for measured claims.


## Governance

- [Contributing](../CONTRIBUTING.md)
- [Security policy](../SECURITY.md)
- [Citation metadata](../CITATION.cff)
- [Changelog](../CHANGELOG.md)

Run make audit for the lightweight local repository audit mirrored by CI.
