# Fish Speech patch artifacts

**Built with Fish Audio.**

The files in this directory are patch artifacts against the pinned upstream Fish Speech source recorded in `references/upstream.lock`.

## Licensing boundary

These patches contain modifications to Fish Speech and may include upstream source lines as patch context. They are therefore **not offered under the repository MIT License**.

The patch artifacts remain governed by the **Fish Audio Research License**, retained at:

`../THIRD_PARTY_LICENSES/FISH-AUDIO-RESEARCH-LICENSE`

The MIT License in the repository root applies only to original repository-authored material that is not derived from or modifying Fish Audio Materials.

## Modification scope

The retained patches change the pinned Fish Speech source to support the qualified Kaggle T4x2 runtime, including:

- explicit semantic-model and decoder device placement;
- configurable `max_seq_len`;
- reference-audio encoding on the decoder device;
- explicit transfer of generated VQ codes to the decoder device before audio decoding;
- local API arguments for separate semantic and decoder devices;
- decoder precision/dtype handling;
- reduced API warm-up token count for the qualified runtime.

The cumulative API patch includes the earlier CLI dual-GPU changes plus API-specific split-device handling.

## Upstream attribution

Fish Speech and Fish Audio S2 Pro remain Fish Audio materials. This repository does not claim ownership of upstream Fish Speech source code or Fish Audio model weights.

See `../NOTICE.txt` and `../LICENSE-NOTES.md` for the complete repository licensing boundary.
