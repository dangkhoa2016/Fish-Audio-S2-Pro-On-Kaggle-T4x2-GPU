#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "PROJECT_ROOT=$ROOT"
echo "UPSTREAM_COMMIT=$(grep '^UPSTREAM_COMMIT=' references/upstream.lock | cut -d= -f2)"

mkdir -p results evidence
python scripts/inventory_model.py --search-root /kaggle/input --output results/model-manifest.json

echo "Bootstrap preparation complete."
echo "Run scripts/preflight.sh after switching the Kaggle accelerator to GPU T4 x2."
