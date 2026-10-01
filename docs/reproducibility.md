# Reproducibility Guide

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](reproducibility.vi.md)

This guide is the operational entry point for reproducing the qualified Fish Audio S2 Pro paths from a fresh Kaggle session. It explains not only what to run, but why each repository file exists, which operating path it belongs to, and what evidence it is expected to produce.

## Required environment

- Kaggle notebook with GPU accelerator set to **T4 x2** for the dual-GPU and concurrency paths.
- Fish Audio S2 Pro Kaggle model attachment.
- VoxCPM2 Kaggle model attachment only when reproducing the independent synthetic multi-speaker acceptance.
- Internet access during bootstrap when dependencies or the pinned upstream source must be fetched.
- A clean checkout of this repository.

The single-T4 INT8 paths use one Tesla T4 at a time. The dual-T4 FP16 and two-instance concurrency paths require both T4 GPUs.

## Reproducibility contract

A reproduction is valid only when it begins from a clean repository checkout and uses the pinned upstream Fish Speech revision recorded in `references/upstream.lock`.

Do not substitute an arbitrary newer upstream commit and still call the result equivalent to the qualified release. Model weights remain outside Git and are mounted from Kaggle.

## Repository areas used during reproduction

| Path | Purpose |
|---|---|
| `scripts/` | executable setup, inference, qualification, benchmark, verification, and reporting entry points |
| `patches/` | repository-owned changes applied to the pinned upstream Fish Speech checkout |
| `references/` | source/model provenance, upstream pin, and synthetic-reference source records |
| `results/` | machine-readable summaries and retained result artifacts |
| `evidence/` | runtime logs and supporting execution evidence |
| `reports/` | reviewer-facing generated reports such as the listening comparison HTML |
| `docs/` | human-readable architecture, methodology, qualification, and release records |

## Core bootstrap sequence

Run these commands first in a fresh Kaggle session:

```bash
./scripts/bootstrap_kaggle.sh
./scripts/preflight.sh
./scripts/setup_runtime.sh
./scripts/apply_upstream_patch.sh
```

### `scripts/bootstrap_kaggle.sh`

**Purpose:** establish the canonical working environment from a fresh Kaggle session.

It checks out the exact Fish Speech revision pinned in `references/upstream.lock`, prepares the expected repository/runtime layout, and discovers the attached Fish Audio S2 Pro model.

**Use it when:** starting any clean reproduction.

**Expected result:** pinned upstream source and model paths are available for the later setup and qualification steps.

### `scripts/preflight.sh`

**Purpose:** reject an unsupported or incomplete environment before expensive model loading.

It verifies the expected Kaggle GPU topology and basic runtime prerequisites.

**Use it when:** immediately after bootstrap and before setup.

**Expected result:** the T4/T4x2 environment required by the selected path is confirmed, or the run fails early with an actionable error.
### `scripts/setup_runtime.sh`

**Purpose:** install and prepare the Python/runtime dependencies required by the pinned Fish Speech source and repository runners.

**Use it when:** after preflight in a fresh session.

**Expected result:** the runtime is ready for model inventory, patch application, inference, and qualification.

### `scripts/inventory_model.py`

**Purpose:** inspect the attached Fish Audio S2 Pro model payload and record the model inventory used by the qualification flow.

**Use it when:** validating model attachment/provenance or debugging a missing/incomplete model mount.

**Expected result:** a deterministic inventory of the available model artifacts.

### `scripts/apply_upstream_patch.sh`

**Purpose:** apply the repository-owned compatibility/runtime patch set to the exact pinned Fish Speech checkout.

**Use it when:** after runtime setup and before the qualified inference paths.

**Expected result:** the upstream checkout contains the device-placement and repository-specific changes required by the validated Kaggle paths.

## Dual-T4 FP16 path

### `scripts/run_dual_gpu_fp16.sh`

**Purpose:** run the canonical dual-T4 FP16 CLI synthesis path.

GPU0 hosts the Dual-AR/text-to-semantic model and KV cache; GPU1 hosts the codec/reference/audio-decoder side. The two T4 GPUs are not treated as pooled memory.

**Use it when:** reproducing the primary FP16 inference baseline.

**Expected output:** a non-empty WAV file plus runtime logs. A successful process exit without the expected WAV is not considered PASS.
### `scripts/qualify_text_synthesis.py`

**Purpose:** qualify English and Vietnamese text-only synthesis across the retained bilingual text-synthesis cases.

**Use it when:** reproducing bilingual text synthesis acceptance.

**Expected outputs:** structured bilingual text-synthesis results, retained WAV files, and evidence corresponding to `docs/bilingual-text-synthesis.md`.

### `scripts/qualify_voice_cloning.py`

**Purpose:** reproduce the original technical synthetic-reference voice-cloning matrix.

**Use it when:** reviewing the technical voice-cloning path.

**Important:** this is retained as a technical milestone, but it is not the strongest final speaker-cloning authority because the final release gate uses an independent VoxCPM2 reference bank.

### `scripts/run_api_server_dual_gpu.sh`

**Purpose:** launch the qualified local HTTP API on the dual-T4 FP16 topology.

**Use it when:** reproducing the qualified local API behavior.

**Expected behavior:** health, text synthesis, reference handling, cloning, and documented rejection paths behave as recorded in `docs/local-api-qualification.md`.

## Controlled benchmark

### `scripts/run_controlled_benchmark.py`

**Purpose:** execute the controlled FP16 benchmark under the locked baseline.

The benchmark uses batch size 1, `max_seq_len=4096`, `torch.compile` disabled, two warmups, eight scenarios, and five measured runs per scenario.

**Use it when:** reproducing the published wall-time, audio-duration, RTF, semantic-throughput, and memory observations.

**Authority:** see `docs/benchmark-methodology.md`, `docs/controlled-benchmark-results.md`, `results/controlled-benchmark/`, and `evidence/controlled-benchmark.log.gz`.
## Single-T4 INT8 path

### `scripts/quantize_single_t4_int8.py`

**Purpose:** build the weight-only INT8 semantic checkpoint used by the single-T4 capacity path.

The codec remains FP16. This optimization targets memory capacity, not speed.

**Use it when:** the INT8 checkpoint is not already available in the current session.

**Expected output:** the converted semantic checkpoint and conversion metadata used by the single-T4 INT8 path.

### `scripts/run_single_t4_int8.sh`

**Purpose:** run complete TTS on one Tesla T4 using the INT8 semantic model plus FP16 codec.

**Use it when:** reproducing single-T4 INT8 inference.

**Expected result:** a valid non-empty WAV with peak VRAM and semantic throughput consistent with the documented capacity-oriented profile.

### `scripts/run_api_server_single_t4_int8.sh`

**Purpose:** expose the single-T4 INT8 path through the local API runner.

**Use it when:** reproducing the isolated API instance used by the dual-instance concurrency design.

## Two independent T4 instances

The dual-instance concurrency mode runs one complete INT8 API process on GPU0 and one on GPU1. This is two independent services, not one model sharded across pooled 32 GB VRAM.

Exact launch and measurement commands are documented in `docs/dual-instance-concurrency.md`.

The clean-room authority reproduced approximately `2.0126x` aggregate scaling for the tested deterministic request.
## Independent synthetic multi-speaker path

The final release voice-cloning gate intentionally uses references generated by a different model so S2 Pro is not evaluated against a reference bank produced by itself.

### `scripts/setup_voxcpm2_reference_runtime.sh`

**Purpose:** prepare the independent VoxCPM2 runtime used only for synthetic reference generation.

**Use it when:** reproducing the final multi-speaker acceptance from scratch.

### `scripts/generate_synthetic_speaker_bank.py`

**Purpose:** generate the eight-speaker reference bank: four English and four Vietnamese synthetic speakers with intentionally varied vocal profiles.

**Expected output:** the reference WAV bank and `results/synthetic-speaker-bank/summary.json`.

### `scripts/qualify_synthetic_multispeaker.py`

**Purpose:** run S2 Pro cloning against the independent reference bank.

**Coverage:** eight same-language cases plus four cross-language cases.

**Expected output:** twelve technical clone outputs and `results/synthetic-multispeaker-acceptance/summary.json`.

### `scripts/score_synthetic_speakers.py`

**Purpose:** perform independent speaker discrimination with the WavLM-based speaker encoder.

**Acceptance rule:** each clone is compared with all eight references; the intended source speaker must rank top-1.

**Qualified result:** 12/12 intended speakers ranked top-1.
### `scripts/check_synthetic_repeatability.py`

**Purpose:** verify deterministic repeatability for the retained repeat cases.

**Acceptance rule:** regenerated outputs must be byte-identical to the authority outputs.

**Qualified result:** 2/2 byte-identical repeats.

### `scripts/build_synthetic_review_html.py`

**Purpose:** generate a reviewer-friendly side-by-side listening page.

**Output:** `reports/synthetic-multispeaker-review.html`.

This report is a listening aid. Human listening is an optional spot-check, not the machine-readable release gate.

## How results and evidence are organized

- `results/` contains structured summaries used as authority for measured claims.
- `evidence/` contains execution logs and supporting runtime evidence.
- `reports/` contains reviewer-facing generated material.
- Capability-specific Markdown documents under `docs/` explain the methodology and interpretation.

Narrative documentation may summarize the results, but it must not override contradictory machine-readable authority artifacts.

## Acceptance discipline

- A runner must not report PASS unless the expected output exists and is non-empty.
- For audio-producing paths, the expected WAV must exist and contain data before PASS.
- Runtime metrics, hashes, and relevant metadata are captured before conclusions are written.
- Secrets and model weights must not enter Git.
- A clean-room failure overrides an earlier development-session success until the reproducibility defect is corrected.
- Tested behavior must not be generalized to untested hardware, settings, speakers, or workloads.

## Repository verification

Before release or after a documentation/runtime change, run:

```bash
make audit
```

The lightweight audit checks shell syntax, Python compilation, JSON validity, internal Markdown links, model-weight policy, whitespace, and common secret patterns. GPU-dependent qualification remains separate because CI does not provide the Kaggle T4x2 hardware baseline.

## Related documents

- [Engineering overview](engineering-overview.md)
- [Qualification matrix](qualification-matrix.md)
- [Evidence index](evidence-index.md)
- [Architecture](architecture.md)
- [Benchmark methodology](benchmark-methodology.md)
- [Troubleshooting](troubleshooting.md)
- [Final release readiness](final-release-readiness.md)
