#!/usr/bin/env python3
import argparse, hashlib, json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

IMPORTANT = {
    "model-00001-of-00002.safetensors",
    "model-00002-of-00002.safetensors",
    "model.safetensors.index.json",
    "codec.pth", "config.json", "tokenizer.json", "tokenizer_config.json",
}

def sha256(path: Path, chunk=16 * 1024 * 1024):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()

def record(path: Path):
    return {"path": str(path), "name": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--search-root", default="/kaggle/input")
    ap.add_argument("--output", default="results/model-manifest.json")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    root = Path(args.search_root)
    candidate_dirs = []
    for codec in root.rglob("codec.pth"):
        parent = codec.parent
        names = {p.name for p in parent.iterdir() if p.is_file()}
        if IMPORTANT.issubset(names):
            candidate_dirs.append(parent)

    candidate_dirs = sorted(set(candidate_dirs))
    if len(candidate_dirs) > 1:
        raise RuntimeError(f"Ambiguous model inventory; multiple complete model directories: {candidate_dirs}")

    if candidate_dirs:
        model_dir = candidate_dirs[0]
        files = sorted(model_dir / name for name in IMPORTANT)
        found = {p.name for p in files if p.is_file()}
    else:
        model_dir = None
        files = sorted(p for p in root.rglob("*") if p.is_file() and p.name in IMPORTANT)
        found = {p.name for p in files}

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        records = list(pool.map(record, files))
    payload = {
        "search_root": str(root),
        "model_dir": str(model_dir) if model_dir else None,
        "status": "PASS" if model_dir and IMPORTANT.issubset(found) else "INCOMPLETE",
        "expected_files": sorted(IMPORTANT),
        "missing_files": sorted(IMPORTANT - found),
        "files": records,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    if payload["status"] != "PASS":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
