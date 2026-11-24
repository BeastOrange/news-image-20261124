#!/usr/bin/env python3
"""Standard library only; copies entry.png next to it to /output/entry.png and prints the byte size."""
import os
import shutil
from pathlib import Path


def main():
    base = Path(__file__).resolve().parent
    src = base / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    size = dst.stat().st_size
    print(f"Copied {src.name} to {dst} ({size} bytes)")


if __name__ == "__main__":
    main()
