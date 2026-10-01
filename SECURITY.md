# Security Policy

## Supported release

The current supported release is `v1.0.0`.

## Reporting

Please report security issues privately through GitHub's repository security reporting features when available. Do not open a public issue containing credentials, tokens, private audio, or other sensitive material.

## Repository security boundaries

This repository must never contain:

- GitHub, Hugging Face, Kaggle, or cloud credentials;
- private keys or authentication headers;
- model weights that are distributed separately;
- private real-human reference audio;
- credential-bearing remote URLs.

Runtime credentials should be supplied only through ephemeral environment or filesystem mechanisms appropriate to the execution platform.

## Evidence privacy

The retained public audio corpus is synthetic. Optional private real-human evaluation is outside the release requirement and should remain outside Git history.

## Dependency and upstream scope

The project pins the Fish Speech upstream revision used for qualification. Security issues in upstream runtime or model dependencies should also be reported to their respective maintainers.
