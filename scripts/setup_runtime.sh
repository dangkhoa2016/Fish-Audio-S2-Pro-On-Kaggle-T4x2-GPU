#!/usr/bin/env bash
set -euo pipefail
UPSTREAM_DIR="${UPSTREAM_DIR:-/kaggle/working/fish-speech-upstream}"
CACHE_DIR="${UV_CACHE_DIR:-/kaggle/working/.uv-cache}"
cd "$UPSTREAM_DIR"
UV_CACHE_DIR="$CACHE_DIR" uv sync --extra cu128 --no-install-package pyaudio
UV_CACHE_DIR="$CACHE_DIR" uv pip install --python .venv/bin/python wrapt
echo "RUNTIME_SETUP=PASS"
