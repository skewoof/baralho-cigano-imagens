#!/usr/bin/env python3
from pathlib import Path
import csv
import argparse

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

def iter_images(indir: Path):
    for p in sorted(indir.iterdir()):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            yield p

def main():
    ap = argparse.ArgumentParser(description="Gera CSV com links raw do GitHub para imagens.")
    ap.add_argument("--indir", required=True, help="Pasta das imagens (ex: imagens/cigano_cropped)")
    ap.add_argument("--repo", required=True, help="Repo no formato owner/repo")
    ap.add_argument("--branch", default="main", help="Branch (default: main)")
    ap.add_argument("--prefix", required=True, help="Caminho das imagens no repo (ex: imagens/cigano_cropped)")
    ap.add_argument("--outcsv", required=True, help="CSV de saída (ex: cigano_cropped_links.csv)")
    args = ap.parse_args()

    indir = Path(args.indir).resolve()
    if not indir.exists():
        raise SystemExit(f"Pasta não encontrada: {indir}")

    base = f"https://raw.githubusercontent.com/{args.repo}/{args.branch}"

    rows = []
    for img in iter_images(indir):
        url = f"{base}/{args.prefix}/{img.name}"
        rows.append((img.name, url))

    outcsv = Path(args.outcsv).resolve()
    with outcsv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "url"])
        w.writerows(rows)

    print("✅ CSV de links gerado com sucesso!")
    print(f"📄 Arquivo: {outcsv}")
    print(f"🔗 Total de imagens: {len(rows)}")

if __name__ == "__main__":
    main()
