#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from collections import Counter

from PIL import Image


IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


@dataclass(frozen=True)
class Rec:
    file: str
    width: int
    height: int
    mode: str
    fmt: str


def iter_images(indir: Path):
    for p in sorted(indir.rglob("*")):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", required=True, help="Pasta com imagens (ex.: imagens/cigano)")
    ap.add_argument("--outdir", required=True, help="Pasta de relatórios (ex.: reports)")
    args = ap.parse_args()

    indir = Path(args.indir).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    rows: list[Rec] = []
    errors = 0

    for img_path in iter_images(indir):
        try:
            with Image.open(img_path) as im:
                w, h = im.size
                rows.append(Rec(
                    file=str(img_path.relative_to(indir)),
                    width=w,
                    height=h,
                    mode=str(im.mode),
                    fmt=str(im.format or "")
                ))
        except Exception:
            errors += 1

    sizes = Counter((r.width, r.height) for r in rows)

    csv1 = outdir / "cigano_image_sizes.csv"
    csv2 = outdir / "cigano_image_sizes_summary.csv"

    with csv1.open("w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["file", "width", "height", "mode", "format"])
        for r in rows:
            wr.writerow([r.file, r.width, r.height, r.mode, r.fmt])

    with csv2.open("w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["width", "height", "count"])
        for (w, h), c in sizes.most_common():
            wr.writerow([w, h, c])

    print("OK!")
    print(f"- {csv1}")
    print(f"- {csv2}")
    print(f"Total imagens: {len(rows)} (sem contar erros).")
    if errors:
        print(f"Erros ao abrir: {errors}")


if __name__ == "__main__":
    main()
