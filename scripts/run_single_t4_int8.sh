#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_DIR="${UPSTREAM_DIR:-/kaggle/working/fish-speech-upstream}"
MODEL_DIR="${MODEL_DIR:-/tmp/fish-s2-pro-int8}"
TEXT="${1:-Hello from Fish Audio S2 Pro.}"
OUT="${2:-$ROOT/results/single-t4-int8/sample.wav}"
MAX_NEW_TOKENS="${MAX_NEW_TOKENS:-96}"

test -f "$MODEL_DIR/model.pth"
test -e "$MODEL_DIR/codec.pth"
mkdir -p "$(dirname "$OUT")"

cd "$UPSTREAM_DIR"
.venv/bin/python fish_speech/models/text2semantic/inference.py   --text "$TEXT"   --checkpoint-path "$MODEL_DIR"   --device cuda:0   --decoder-device cuda:0   --max-seq-len 4096   --max-new-tokens "$MAX_NEW_TOKENS"   --half --no-compile   --output "$OUT"   --output-dir "$(dirname "$OUT")"

echo "SINGLE_T4_INT8=PASS"
