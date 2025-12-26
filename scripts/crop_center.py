#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

# ================= CONFIG =================
INPUT_DIR = Path("images/cigano")
OUTPUT_DIR = Path("images/cigano_cropped")

TARGET_WIDTH = 683
TARGET_HEIGHT = 1024
ASPECT_RATIO = TARGET_WIDTH / TARGET_HEIGHT  # ≈ 0.666
# ==========================================

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

def iter_images():
    for p in sorted(INPUT_DIR.iterdir()):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            yield p

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    cropped = 0
    kept = 0

    for img_path in iter_images():
        total += 1
        out_path = OUTPUT_DIR / img_path.name

        with Image.open(img_path) as im:
            im = im.convert("RGBA")
            w, h = im.size

            # 🔑 largura ideal baseada na ALTURA TOTAL
            ideal_w = int(h * ASPECT_RATIO)

            if w > ideal_w:
                # ✂️ recorte SOMENTE horizontal, centralizado
                left = (w - ideal_w) // 2
                right = left + ideal_w
                out = im.crop((left, 0, right, h))
                cropped += 1
                print(f"✂️ {img_path.name}: {w}x{h} → {ideal_w}x{h}")
            else:
                # ✅ já está no formato certo
                out = im
                kept += 1
                print(f"✅ {img_path.name}: mantida ({w}x{h})")

            # 🔁 padroniza tamanho final (opcional, mas recomendado)
            out = out.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            out.save(out_path, format="PNG", optimize=True)

    print("\n=== RESUMO ===")
    print(f"Total: {total}")
    print(f"Recortadas (folha): {cropped}")
    print(f"Mantidas (já carta): {kept}")
    print(f"Saída em: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
