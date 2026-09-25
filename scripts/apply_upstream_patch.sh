#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_DIR="${UPSTREAM_DIR:-/kaggle/working/fish-speech-upstream}"
PATCH="$ROOT/patches/dual-gpu/0001-dual-gpu-decoder-and-seq-len.patch"
cd "$UPSTREAM_DIR"
if git apply --check "$PATCH" >/dev/null 2>&1; then
  git apply "$PATCH"
  echo "PATCH_APPLIED=PASS"
elif git apply --reverse --check "$PATCH" >/dev/null 2>&1; then
  echo "PATCH_ALREADY_APPLIED=PASS"
else
  echo "PATCH_STATE=FAIL" >&2
  exit 1
fi
