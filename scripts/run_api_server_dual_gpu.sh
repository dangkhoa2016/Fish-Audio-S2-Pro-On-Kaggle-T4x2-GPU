#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_DIR="${UPSTREAM_DIR:-/kaggle/working/fish-speech-upstream}"
MODEL_DIR="${MODEL_DIR:-/kaggle/input/models/dangkhoa2016/fishaudio-s2-pro/pytorch/default/1}"
LISTEN="${LISTEN:-127.0.0.1:8080}"

cd "$UPSTREAM_DIR"
exec .venv/bin/python tools/api_server.py   --llama-checkpoint-path "$MODEL_DIR"   --decoder-checkpoint-path "$MODEL_DIR/codec.pth"   --device cuda:0   --decoder-device cuda:1   --max-seq-len 4096   --half   --listen "$LISTEN"   --workers 1   --max-text-length 500
