# Contributing

Thank you for improving this repository. Contributions should preserve the project's evidence-first and reproducibility-oriented engineering style.

## Before opening a change

- Read `PROJECT-CONTRACT.md` and `docs/README.md`.
- Keep the Fish Speech upstream pin explicit.
- Do not commit model weights, credentials, private voice data, or generated caches.
- Do not broaden performance or quality claims beyond retained evidence.

## Change expectations

A technical change should include:

1. the problem being solved;
2. the hardware/runtime configuration affected;
3. reproduction or validation commands;
4. machine-readable evidence when the change affects measured behavior;
5. documentation updates when public behavior or scope changes.

## Commit style

Use imperative, engineering-focused subjects. Keep commits scoped to one coherent milestone. Commit bodies should explain why the change exists and what was validated, not merely list filenames.

## Validation

Run the repository audit workflow or equivalent local checks before submitting a change. GPU-dependent behavior must be validated on the documented hardware before it is described as qualified.

## Pull requests

Describe the tested configuration, expected impact, retained evidence, and any known limitations. A passing static audit does not substitute for GPU qualification when runtime behavior changes.
