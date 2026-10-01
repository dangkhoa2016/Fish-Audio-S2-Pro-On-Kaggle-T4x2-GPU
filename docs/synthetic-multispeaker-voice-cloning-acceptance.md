# Synthetic Multi-Speaker Voice-Cloning Acceptance

Status: **PASS — reproducible technical, speaker-discrimination, and repeatability gates**

## Scope

The final reproducible voice-cloning gate uses an independent TTS model, OpenBMB VoxCPM2, to generate a synthetic speaker bank. No real-person voice is required.

This benchmark evaluates Fish Audio S2 Pro speaker conditioning across multiple synthetic speakers in English and Vietnamese. It does **not** claim universal equivalence to evaluation on arbitrary real-human voices.

## Reference generator

- Model: `openbmb/VoxCPM2`
- Kaggle mirror: `dangkhoa2016/openbmb-voxcpm2`
- Resolved upstream commit: `32279effe8c19989596f05d353d1447f51d9e915`
- Python package used: `voxcpm==2.0.3`
- Mode: Voice Design
- Output: 48 kHz mono
- `cfg_value=2.0`
- `inference_timesteps=10`

The model card and mirror provenance identify VoxCPM2 as Apache-2.0.

## Canonical speaker bank

| ID | Language | Reference duration | Clipping |
|---|---|---:|---:|
| en-f01 | EN | 14.24 s | 0 |
| en-f02 | EN | 14.72 s | 0 |
| en-m01 | EN | 13.12 s | 0 |
| en-m02 | EN | 16.00 s | 0 |
| vi-f01 | VI | 13.44 s | 0 |
| vi-f02 | VI | 14.88 s | 0 |
| vi-m01 | VI | 14.40 s | 0 |
| vi-m02 | VI | 14.24 s | 0 |

Descriptions intentionally vary gender presentation, age, timbre, energy, and pacing. Exact reference transcripts and SHA-256 values are retained in `results/synthetic-speaker-bank/summary.json`.

## S2 Pro matrix

S2 Pro runs with the accepted dual-T4 FP16 topology:

- GPU0: semantic / Dual-AR / KV cache
- GPU1: codec / reference encoder / decoder
- `max_seq_len=4096`
- `torch.compile=OFF`

The model and codec are loaded once; all eight references are encoded once.

Acceptance cases:

- 8 same-language clones;
- 4 cross-language clones:
  - `en-f01 -> VI`
  - `en-m02 -> VI`
  - `vi-f01 -> EN`
  - `vi-m02 -> EN`

Result: **12 / 12 technical cases PASS**.

Aggregate technical results:

- mean output duration: about 9.973 s
- output duration range: about 8.266–11.471 s
- mean RTF: about 2.711
- RTF range: about 2.693–2.774
- maximum clipping ratio: 0
- peak allocated GPU0: 10,948,754,944 bytes
- peak allocated GPU1: 4,826,770,944 bytes
- no OOM
- no device mismatch

## Independent speaker-discrimination evidence

Verifier:

- `microsoft/wavlm-base-plus-sv`
- pinned revision: `feb593a6c23c1cc3d9510425c29b0a14d2b07b1e`
- WavLM x-vector embeddings
- normalized cosine similarity

Each S2 Pro output is compared against **all eight** VoxCPM2 references. No arbitrary absolute cosine threshold is used. The test asks whether the intended speaker ranks first among the complete reference bank.

Results:

- overall top-1: **12 / 12**
- same-language top-1: **8 / 8**
- cross-language top-1: **4 / 4**
- mean intended-speaker cosine: **0.96917**
- mean margin over best impostor: **0.14344**
- minimum margin over best impostor: **0.03186** (still positive)

This is relative speaker-identification evidence, not an absolute perceptual-quality score.

## Deterministic repeatability

Two representative same-language cases were regenerated from a fresh S2 Pro model load with the same input and seed:

- `en-f01-same`
- `vi-f01-same`

Result: **2 / 2 byte-identical**.

For both cases:

- output byte count matched exactly;
- SHA-256 matched exactly.

## Listening review

`reports/synthetic-multispeaker-review.html` provides side-by-side audio players for:

- each VoxCPM2 reference;
- each same-language S2 Pro clone;
- cross-language clones where selected;
- deterministic repeats where selected.

A human listening spot-check remains useful for naturalness, pronunciation, and obvious artifacts, but no real-person voice is needed.

## Reproduction

1. Attach both Kaggle models:
   - `dangkhoa2016/fishaudio-s2-pro`
   - `dangkhoa2016/openbmb-voxcpm2`
2. Run `scripts/setup_voxcpm2_reference_runtime.sh`.
3. Generate references with `scripts/generate_synthetic_speaker_bank.py`.
4. Bootstrap Fish Speech with `scripts/bootstrap_kaggle.sh`.
5. Run `scripts/setup_runtime.sh` and `scripts/apply_upstream_patch.sh`.
6. Run `scripts/qualify_synthetic_multispeaker.py`.
7. Run `scripts/score_synthetic_speakers.py`.
8. Run `scripts/check_synthetic_repeatability.py`.
9. Run `scripts/build_synthetic_review_html.py`.

## Authority artifacts

- `results/synthetic-speaker-bank/summary.json`
- `results/synthetic-multispeaker-acceptance/summary.json`
- `results/synthetic-multispeaker-acceptance/speaker-verification.json`
- `results/synthetic-multispeaker-repeatability/summary.json`
- `evidence/synthetic-speaker-bank.log`
- `evidence/synthetic-multispeaker-acceptance.log`
- `evidence/synthetic-speaker-verification.log`
- `evidence/synthetic-multispeaker-repeatability.log`

## Acceptance boundary

This gate supersedes the previously planned mandatory real-human-reference release gate.

Optional private real-human evaluation may still be performed as an additional experiment, but it is not required for this repository's reproducible release qualification.
