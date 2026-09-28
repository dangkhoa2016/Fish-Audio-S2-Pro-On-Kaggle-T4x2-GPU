#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from pathlib import Path

import torch

UPSTREAM_DIR = Path(os.environ.get("UPSTREAM_DIR", "/kaggle/working/fish-speech-upstream"))
sys.path.insert(0, str(UPSTREAM_DIR))

from fish_speech.models.text2semantic.inference import init_model
from tools.llama.quantize import WeightOnlyInt8QuantHandler

WEIGHT_FILES = {
    "codec.pth",
    "model.safetensors",
    "model.safetensors.index.json",
    "model-00001-of-00002.safetensors",
    "model-00002-of-00002.safetensors",
}


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--max-seq-len", type=int, default=4096)
    ap.add_argument("--codec-mode", choices=("symlink", "copy", "omit"), default="symlink")
    ap.add_argument("--force", action="store_true")
    return ap.parse_args()


def prepare_output(src: Path, dst: Path, codec_mode: str, force: bool) -> None:
    if "int8" not in str(dst).lower():
        raise ValueError("Output path must contain 'int8' because upstream loader selects INT8 by path name.")
    if dst.exists():
        if not force:
            raise FileExistsError(f"{dst} exists; pass --force to replace it")
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    for item in src.iterdir():
        if not item.is_file() or item.name in WEIGHT_FILES:
            continue
        shutil.copy2(item, dst / item.name)

    codec = src / "codec.pth"
    if codec_mode == "symlink":
        (dst / "codec.pth").symlink_to(codec.resolve())
    elif codec_mode == "copy":
        shutil.copy2(codec, dst / "codec.pth")


def main() -> None:
    args = parse_args()
    src = args.source.resolve()
    dst = args.output.resolve()
    prepare_output(src, dst, args.codec_mode, args.force)

    print("SINGLE_T4_INT8_CONVERT_START", flush=True)
    started = time.time()
    model, _ = init_model(
        src, device="cpu", precision=torch.bfloat16,
        compile=False, max_seq_len=args.max_seq_len
    )
    print(f"SOURCE_MODEL_LOADED_S={time.time() - started:.3f}", flush=True)

    quantized = WeightOnlyInt8QuantHandler(model).create_quantized_state_dict()
    int8_count = sum(
        isinstance(v, torch.Tensor) and v.dtype == torch.int8
        for v in quantized.values()
    )
    bf16_count = sum(
        isinstance(v, torch.Tensor) and v.dtype == torch.bfloat16
        for v in quantized.values()
    )

    output_weights = dst / "model.pth"
    torch.save(quantized, output_weights)

    if (dst / "model.safetensors.index.json").exists():
        raise RuntimeError("Unexpected safetensors index in INT8 output")

    print(f"STATE_TENSORS={len(quantized)}")
    print(f"INT8_TENSORS={int8_count}")
    print(f"BF16_TENSORS={bf16_count}")
    print(f"MODEL_PTH_BYTES={output_weights.stat().st_size}")
    print(f"OUTPUT={dst}")
    print(f"TOTAL_S={time.time() - started:.3f}")
    print("SINGLE_T4_INT8_CONVERT=PASS")


if __name__ == "__main__":
    main()
