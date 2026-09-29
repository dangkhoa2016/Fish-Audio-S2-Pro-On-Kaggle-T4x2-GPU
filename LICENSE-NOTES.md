# License notes

This repository uses **scoped licensing**. The MIT License and the Fish Audio Research License do not apply to the same material.

## Repository-authored material — MIT

Original material authored specifically for this repository is licensed under the [MIT License](LICENSE), unless a file explicitly states otherwise.

This includes repository-authored:

- setup and orchestration scripts;
- benchmark and qualification tooling;
- CI / audit configuration;
- repository governance files;
- documentation and reports authored for this project.

MIT copyright holder:

`Đăng Khoa <i.am@dangkhoa.dev>`

## Fish Audio materials — Fish Audio Research License

The following are **not relicensed under MIT**:

- Fish Audio S2 Pro model weights;
- upstream Fish Speech source code and documentation;
- portions of upstream Fish Speech source reproduced as patch context;
- patch artifacts under `patches/` that modify Fish Speech;
- other Fish Audio Materials or Derivative Works as defined by the Fish Audio Research License.

These materials remain governed by the **Fish Audio Research License**. A retained copy is available at:

`THIRD_PARTY_LICENSES/FISH-AUDIO-RESEARCH-LICENSE`

The retained license permits research and non-commercial use subject to its terms. Commercial use of Fish Audio Materials or Derivative Works requires a separate written license from Fish Audio.

## Patch artifacts

The files under `patches/` describe modifications to the pinned Fish Speech source. To avoid implying that upstream Fish Speech code or derivative modifications are being relicensed, those patch artifacts are treated as governed by the Fish Audio Research License rather than the repository MIT License.

See [patches/README.md](patches/README.md) for the modification scope.

## Distribution and attribution

When this repository distributes Fish Audio-derived patch material, the repository retains:

1. a copy of the Fish Audio Research License;
2. the required Fish Audio attribution notice in `NOTICE.txt`;
3. the required **Built with Fish Audio** attribution in project documentation;
4. a description of how the retained patch artifacts modify Fish Speech.

The exact Fish Speech revision used by this project is pinned in `references/upstream.lock`.

## Model weights

Fish Audio S2 Pro model weights are not committed to this Git repository. The project references an external Kaggle mirror for reproducible execution. Any redistribution of those weights remains subject to the Fish Audio Research License and applicable platform terms.

## Third-party components

Third-party libraries, models, and tools used by the project remain governed by their own licenses. The repository MIT License does not supersede those licenses.

Before using, redistributing, or deploying this project, review the license terms that apply to each component and your intended use.
