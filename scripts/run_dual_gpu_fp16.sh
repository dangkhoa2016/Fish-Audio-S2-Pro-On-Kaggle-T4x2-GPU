#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_DIR="${UPSTREAM_DIR:-/kaggle/working/fish-speech-upstream}"
MODEL_DIR="${MODEL_DIR:-/kaggle/input/models/dangkhoa2016/fishaudio-s2-pro/pytorch/default/1}"
TEXT="${1:-Hello from Fish Audio S2 Pro.}"
OUT="${2:-$ROOT/results/dual-gpu/sample.wav}"
if [[ "$OUT" != /* ]]; then OUT="$PWD/$OUT"; fi
mkdir -p "$(dirname "$OUT")" "$ROOT/evidence"
cd "$UPSTREAM_DIR"
.venv/bin/python fish_speech/models/text2semantic/inference.py   --text "$TEXT"   --checkpoint-path "$MODEL_DIR"   --device cuda:0   --decoder-device cuda:1   --max-seq-len 4096   --half --no-compile   --output "$OUT"   --output-dir "$(dirname "$OUT")"
test -s "$OUT"
echo "DUAL_GPU_FP16=PASS"
