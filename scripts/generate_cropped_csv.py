#!/usr/bin/env python3
import csv
from pathlib import Path

# ===== CONFIG =====
REPO_OWNER = "skewoof"
REPO_NAME = "baralho-cigano-imagens"
BRANCH = "main"

INPUT_CSV = "cigano_raw.csv"        # CSV que aponta para as imagens originais
OUTPUT_CSV = "cigano_cropped.csv"   # CSV novo (saída)

DECK_COLUMN = "Cigano"
CROPPED_DIR = Path("imagens/cigano_cropped")
# ==================

def raw_url(filename: str) -> str:
    return (
        f"https://raw.githubusercontent.com/"
        f"{REPO_OWNER}/{REPO_NAME}/{BRANCH}/"
        f"imagens/cigano_cropped/{filename}"
    )

def main():
    if not Path(INPUT_CSV).exists():
        print(f"❌ Arquivo não encontrado: {INPUT_CSV}")
        return

    if not CROPPED_DIR.exists():
        print(f"❌ Pasta não encontrada: {CROPPED_DIR}")
        return

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    header = rows[0]
    try:
        deck_idx = header.index(DECK_COLUMN)
    except ValueError:
        print(f"❌ Coluna '{DECK_COLUMN}' não encontrada no CSV.")
        return

    # pega lista ordenada dos arquivos cropped (001.png, 002.png, ...)
    cropped_files = sorted(
        p.name for p in CROPPED_DIR.iterdir()
        if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]
    )

    if not cropped_files:
        print("❌ Nenhuma imagem recortada encontrada.")
        return

    card_idx = 0

    for row_i in range(1, len(rows)):
        row = rows[row_i]

        if card_idx >= len(cropped_files):
            break

        # garante tamanho da linha
        while len(row) <= deck_idx:
            row.append("")

        cell = row[deck_idx].strip()
        if cell.startswith("http"):
            row[deck_idx] = raw_url(cropped_files[card_idx])
            card_idx += 1

        rows[row_i] = row

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✅ CSV de cartas recortadas gerado com sucesso!")
    print(f"📄 Arquivo: {OUTPUT_CSV}")
    print(f"🔗 Apontando para: imagens/cigano_cropped/")

if __name__ == "__main__":
    main()
