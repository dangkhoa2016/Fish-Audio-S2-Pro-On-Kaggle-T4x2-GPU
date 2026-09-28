#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_DIR="${UPSTREAM_DIR:-/kaggle/working/fish-speech-upstream}"
MODEL_DIR="${MODEL_DIR:-/tmp/fish-s2-pro-int8}"
LISTEN="${LISTEN:-127.0.0.1:8091}"

test -f "$MODEL_DIR/model.pth"
test -e "$MODEL_DIR/codec.pth"

cd "$UPSTREAM_DIR"
exec .venv/bin/python tools/api_server.py   --llama-checkpoint-path "$MODEL_DIR"   --decoder-checkpoint-path "$MODEL_DIR/codec.pth"   --device cuda:0   --decoder-device cuda:0   --max-seq-len 4096   --half   --listen "$LISTEN"   --workers 1   --max-text-length 500
