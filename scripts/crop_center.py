#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

INPUT_DIR = Path("images/cigano")
OUTPUT_DIR = Path("images/cigano_cropped")

def main():
    images = sorted(
        p for p in INPUT_DIR.iterdir()
        if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]
    )

    if not images:
        print("❌ Nenhuma imagem encontrada.")
        return

    # Descobre o menor tamanho comum
    widths, heights = [], []
    for img in images:
        with Image.open(img) as im:
            w, h = im.size
            widths.append(w)
            heights.append(h)

    target_w = min(widths)
    target_h = min(heights)

    print(f"🎯 Tamanho alvo: {target_w} x {target_h}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for img in images:
        with Image.open(img) as im:
            w, h = im.size
            left = (w - target_w) // 2
            top = (h - target_h) // 2
            right = left + target_w
            bottom = top + target_h

            cropped = im.crop((left, top, right, bottom))
            out_path = OUTPUT_DIR / img.name
            cropped.save(out_path)

            print(f"✂️ {img.name} → recortada")

    print("\n✅ Recorte finalizado com sucesso!")
    print(f"📁 Resultado em: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
