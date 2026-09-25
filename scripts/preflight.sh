#!/usr/bin/env bash
set -euo pipefail

echo "=== system ==="
python --version
uname -a

echo "=== disk ==="
df -h /kaggle/working || true

echo "=== memory ==="
free -h || true

echo "=== nvidia-smi ==="
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi
else
  echo "nvidia-smi: NOT_AVAILABLE"
fi

echo "=== torch ==="
python - <<'PY'
import torch
print("torch_version=", torch.__version__)
print("torch_cuda_version=", torch.version.cuda)
print("cuda_available=", torch.cuda.is_available())
print("device_count=", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    print(f"device_{i}={p.name}; total_memory={p.total_memory}")
PY
