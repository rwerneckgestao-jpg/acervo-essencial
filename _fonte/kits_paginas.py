# Gera, a partir dos PDFs finais dos kits terapêuticos (renderizados com pdftoppm em PASTA),
# as páginas extras da galeria e a parede com todas as páginas de cada kit.
import glob, os, sys
from PIL import Image
PASTA = sys.argv[1]
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRAS = {"t01": [2, 3, 13, 18, 28, 32, 36, 38], "t02": [2, 4, 5, 8, 16, 24, 29],
          "t03": [2, 3, 7, 12, 13, 20, 22, 28], "t04": [2, 4, 7, 10, 13, 22, 26]}
for k, pags in EXTRAS.items():
    for p in pags:
        Image.open(f"{PASTA}/{k}-{p:02d}.jpg").convert("RGB").save(f"{RAIZ}/img/kits/{k}_pg{p:02d}.jpg", quality=80, optimize=True, progressive=True)
    fs = sorted(glob.glob(f"{PASTA}/{k}-*.jpg"))
    cols = 8; w = 170; h = int(w * 1.414); g = 10
    rows = (len(fs) + cols - 1) // cols
    mural = Image.new("RGB", (cols * (w + g) + g, rows * (h + g) + g), (239, 231, 218))
    for i, f in enumerate(fs):
        mural.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (g + (i % cols) * (w + g), g + (i // cols) * (h + g)))
    mural.save(f"{RAIZ}/img/kits/todas_{k}.jpg", quality=78, optimize=True, progressive=True)
    print(k, len(fs), mural.size)
