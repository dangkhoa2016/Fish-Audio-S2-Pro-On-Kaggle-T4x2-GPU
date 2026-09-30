#!/usr/bin/env bash
set -euo pipefail

TARGET="${VOXCPM_PYLIB:-/kaggle/working/voxcpm2-pylib}"
PACKAGE_VERSION="${VOXCPM_PACKAGE_VERSION:-2.0.3}"

mkdir -p "$TARGET"
python3 -m pip install --target "$TARGET" --upgrade --no-deps "voxcpm==$PACKAGE_VERSION"

PYTHONPATH="$TARGET${PYTHONPATH:+:$PYTHONPATH}" python3 - <<'PY'
import torch
import voxcpm
print("VOXCPM_RUNTIME=PASS")
print("TORCH_VERSION="+torch.__version__)
print("CUDA_AVAILABLE="+str(torch.cuda.is_available()))
print("CUDA_DEVICE_COUNT="+str(torch.cuda.device_count()))
PY

echo "VOXCPM_PYLIB=$TARGET"
echo "Use: PYTHONPATH=$TARGET python3 scripts/generate_synthetic_speaker_bank.py ..."
