#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_DIR="${UPSTREAM_DIR:-/kaggle/working/fish-speech-upstream}"
source "$ROOT/references/upstream.lock"

echo "PROJECT_ROOT=$ROOT"
echo "UPSTREAM_REPO=$UPSTREAM_REPO"
echo "UPSTREAM_COMMIT=$UPSTREAM_COMMIT"

if [ ! -d "$UPSTREAM_DIR/.git" ]; then
  git clone "$UPSTREAM_REPO" "$UPSTREAM_DIR"
fi
git -C "$UPSTREAM_DIR" fetch origin "$UPSTREAM_COMMIT"
git -C "$UPSTREAM_DIR" checkout --detach "$UPSTREAM_COMMIT"
test "$(git -C "$UPSTREAM_DIR" rev-parse HEAD)" = "$UPSTREAM_COMMIT"
echo "UPSTREAM_PIN=PASS"

mkdir -p "$ROOT/results" "$ROOT/evidence"
python "$ROOT/scripts/inventory_model.py" --search-root /kaggle/input --output "$ROOT/results/model-manifest.json"

echo "BOOTSTRAP=PASS"
echo "Run scripts/preflight.sh after switching the Kaggle accelerator to GPU T4 x2."
