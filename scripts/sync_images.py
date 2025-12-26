#!/usr/bin/env python3
import csv
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

# ===== CONFIG =====
REPO_OWNER = "skewoof"
REPO_NAME = "baralho-cigano-imagens"
BRANCH = "main"

INPUT_CSV = "cigano.csv"
OUTPUT_CSV = "cigano_raw.csv"

DECK_COLUMN_NAME = "Cigano"
DECK_SIZE = 36
IMAGES_DIR = Path("imagens/cigano")
# ==================

def is_url(value: str) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))

def infer_extension(url: str, response: requests.Response) -> str:
    path = urlparse(url).path.lower()
    _, ext = os.path.splitext(path)

    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
        return ".jpg" if ext == ".jpeg" else ext

    content_type = (response.headers.get("content-type") or "").lower()
    if "jpeg" in content_type:
        return ".jpg"
    if "webp" in content_type:
        return ".webp"
    return ".png"

def download_image(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, stream=True, timeout=30, headers=headers)
    r.raise_for_status()

    ext = infer_extension(url, r)
    dest = dest.with_suffix(ext)

    tmp = dest.with_suffix(dest.suffix + ".part")
    with open(tmp, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 128):
            if chunk:
                f.write(chunk)
    tmp.replace(dest)

def raw_github_url(relative_path: Path) -> str:
    return (
        f"https://raw.githubusercontent.com/"
        f"{REPO_OWNER}/{REPO_NAME}/{BRANCH}/"
        f"{relative_path.as_posix()}"
    )

def main():
    input_csv = Path(INPUT_CSV)
    if not input_csv.exists():
        print(f"❌ Arquivo não encontrado: {INPUT_CSV}")
        sys.exit(1)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # lê CSV inteiro
    with open(input_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        print("❌ CSV vazio.")
        sys.exit(1)

    header = rows[0]
    try:
        deck_col_index = header.index(DECK_COLUMN_NAME)
    except ValueError:
        print(f"❌ Coluna '{DECK_COLUMN_NAME}' não encontrada.")
        print("Cabeçalho encontrado:", header)
        sys.exit(1)

    # URLs começam a partir da 4ª linha (índice 3), como no seu arquivo
    url_rows = rows[3:]
    urls = []

    for row in url_rows:
        if deck_col_index < len(row) and is_url(row[deck_col_index]):
            urls.append(row[deck_col_index].strip())

    urls = urls[:DECK_SIZE]

    if not urls:
        print("❌ Nenhuma URL encontrada na coluna Cigano.")
        sys.exit(1)

    print(f"🔮 Baixando {len(urls)} cartas do Baralho Cigano…\n")

    saved_relative_paths = []

    for i, url in enumerate(urls, start=1):
        filename = f"{i:03d}.png"
        dest = IMAGES_DIR / filename

        print(f"[{i:02d}/{len(urls)}] {url}")
        download_image(url, dest)

        real_file = next(dest.parent.glob(f"{i:03d}.*"))
        saved_relative_paths.append(real_file)

    # cria novo CSV com links raw
    new_rows = [row[:] for row in rows]

    for i, rel_path in enumerate(saved_relative_paths):
        row_index = 3 + i
        while len(new_rows[row_index]) <= deck_col_index:
            new_rows[row_index].append("")

        new_rows[row_index][deck_col_index] = raw_github_url(rel_path)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    print("\n✅ Concluído com sucesso!")
    print(f"📁 Imagens salvas em: {IMAGES_DIR}")
    print(f"📄 CSV gerado: {OUTPUT_CSV}")
    print("\nAgora é só importar o CSV novo na planilha e commitar no GitHub.")

if __name__ == "__main__":
    main()
