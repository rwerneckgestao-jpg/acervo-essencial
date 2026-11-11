# Gera as imagens da loja a partir das páginas reais dos materiais:
#  img/loja/card_<id>.jpg  (800x1000, vitrine)
#  img/loja/og_<id>.jpg    (1200x630, compartilhamento em redes sociais)
#  video/<id>.mp4          (vídeo demonstrativo folheando páginas reais, 720x900)
# Uso: python3 _fonte/imagens.py PASTA_DAS_FONTES_TTF
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from catalogo import PRODUTOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = sys.argv[1]
GAL = json.load(open(os.path.join(RAIZ, "_fonte/galerias.json")))
os.makedirs(f"{RAIZ}/img/loja", exist_ok=True)
os.makedirs(f"{RAIZ}/video", exist_ok=True)

FUNDOS = {"Kit terapêutico": (236, 229, 219), "Coleção de kits": (227, 233, 228), "Kit de cadernos": (232, 238, 240),
          "App no navegador": (243, 236, 222)}
FUNDO_PADRAO = (246, 239, 227)

def abre(p):
    return Image.open(os.path.join(RAIZ, p)).convert("RGB")

def pagina(img, largura, angulo=0):
    """Página com sombra suave, girada; devolve RGBA."""
    h = int(img.height * largura / img.width)
    pg = img.resize((largura, h), Image.LANCZOS).convert("RGBA")
    m = 40
    base = Image.new("RGBA", (largura + 2 * m, h + 2 * m), (0, 0, 0, 0))
    sombra = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rectangle([m + 6, m + 14, m + largura + 6, m + h + 14], fill=(40, 30, 20, 70))
    sombra = sombra.filter(ImageFilter.GaussianBlur(16))
    base.alpha_composite(sombra)
    base.alpha_composite(pg, (m, m))
    ImageDraw.Draw(base).rectangle([m, m, m + largura - 1, m + h - 1], outline=(0, 0, 0, 28))
    return base.rotate(angulo, resample=Image.BICUBIC, expand=True)

def cola(fundo, peca, cx, cy):
    fundo.alpha_composite(peca, (int(cx - peca.width / 2), int(cy - peca.height / 2)))

def card(p):
    W, H = 800, 1000
    c = Image.new("RGBA", (W, H), FUNDOS.get(p["linha"], FUNDO_PADRAO) + (255,))
    if p.get("capas"):
        capas = p["capas"]
        pos = [(-8, 255, 490), (-3, 355, 470), (3, 450, 485), (8, 545, 510)]
        for (a, x, y), cp in zip(pos, capas):
            cola(c, pagina(abre(cp), 300, a), x, y)
    elif p["id"] == "cal27":
        cola(c, pagina(abre(p["capa"]), 400, -4), 330, 500)
        tel = abre("img/cal27/app_1_mes.jpg")
        cola(c, pagina(tel, 250, 3), 590, 540)
    else:
        cola(c, pagina(abre(p["fundo"]), 430, 5), 500, 470)
        cola(c, pagina(abre(p["capa"]), 450, -3), 340, 520)
    c.convert("RGB").save(f"{RAIZ}/img/loja/card_{p['id']}.jpg", quality=82, optimize=True, progressive=True)

def og(p):
    W, H = 1200, 630
    c = Image.new("RGBA", (W, H), (248, 243, 234, 255))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, 470, H], fill=(23, 74, 94, 255))
    f1 = ImageFont.truetype(f"{FONTES}/fraunces600.ttf", 54)
    f2 = ImageFont.truetype(f"{FONTES}/ss3-600.ttf", 28)
    f3 = ImageFont.truetype(f"{FONTES}/fredoka600.ttf", 30)
    d.text((56, 56), "Acervo Essencial", font=f3, fill=(242, 179, 61))
    # quebra o nome em linhas
    palavras, linhas, atual = p["curto"].split(), [], ""
    for w in palavras:
        if d.textlength((atual + " " + w).strip(), font=f1) > 370:
            linhas.append(atual); atual = w
        else:
            atual = (atual + " " + w).strip()
    linhas.append(atual)
    y = 200
    for l in linhas:
        d.text((56, y), l, font=f1, fill=(255, 253, 249)); y += 66
    preco = "Grátis ou R$ 9,90" if p.get("gratis") else "R$ " + f"{p['preco']:.2f}".replace(".", ",")
    d.text((56, y + 24), f"{p['linha']} · {preco}", font=f2, fill=(232, 222, 205))
    if p.get("capas"):
        for i, cp in enumerate(p["capas"]):
            cola(c, pagina(abre(cp), 230, -6 + 4 * i), 640 + i * 130, 320 + (i % 2) * 20)
    else:
        cola(c, pagina(abre(p["fundo"]), 300, 5), 960, 320)
        cola(c, pagina(abre(p["capa"]), 310, -3), 760, 330)
    c.convert("RGB").save(f"{RAIZ}/img/loja/og_{p['id']}.jpg", quality=84, optimize=True)

def lista_galeria(p):
    g = p["galeria"]
    if isinstance(g, str):
        g = [tuple(x) for x in GAL[g]]
    return g

def video(p):
    """Folheia páginas reais: cada página entra, aproxima devagar e passa para a próxima."""
    g = [x for x in lista_galeria(p) if not x[1].startswith("Página")] or lista_galeria(p)
    paginas = [(p["capa"], p["nome"])] + g[:6]
    W, H, FPS, SEG, TR = 720, 900, 24, 2.2, 0.45
    fonte = ImageFont.truetype(f"{FONTES}/ss3-600.ttf", 30)
    pequena = ImageFont.truetype(f"{FONTES}/ss3-400.ttf", 22)
    quadros = []
    for arq, legenda in paginas:
        img = abre(arq)
        quadros.append((img, legenda))
    def frame(i, t):
        img, leg = quadros[i]
        z = 1.0 + 0.05 * t
        fundo = Image.new("RGBA", (W, H), (239, 231, 218, 255))
        pg = pagina(img, int(500 * z), 0)
        cola(fundo, pg, W / 2, H / 2 - 30)
        d = ImageDraw.Draw(fundo)
        d.rectangle([0, H - 96, W, H], fill=(23, 74, 94, 235))
        d.text((32, H - 84), leg, font=fonte, fill=(255, 253, 249))
        d.text((32, H - 44), "Páginas reais do material · Acervo Essencial", font=pequena, fill=(214, 226, 230))
        return fundo.convert("RGB")
    saida = f"{RAIZ}/video/{p['id']}.mp4"
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "30", "-preset", "slow", "-movflags", "+faststart", "-an", saida], stdin=subprocess.PIPE)
    n = int(SEG * FPS); ntr = int(TR * FPS)
    for i in range(len(quadros)):
        for f in range(n):
            t = f / n
            fr = frame(i, t)
            if f >= n - ntr and i + 1 < len(quadros):
                prox = frame(i + 1, 0)
                fr = Image.blend(fr, prox, (f - (n - ntr)) / ntr)
            proc.stdin.write(fr.tobytes())
    proc.stdin.close(); proc.wait()
    # quadro de capa do vídeo
    frame(1 if len(quadros) > 1 else 0, 0.3).save(f"{RAIZ}/video/{p['id']}.jpg", quality=80, optimize=True)

if __name__ == "__main__":
    so = sys.argv[2:]  # opcional: ids
    for p in PRODUTOS:
        if so and p["id"] not in so: continue
        card(p); og(p)
        if p["id"] not in ("cal27",):
            video(p)
        print("ok", p["id"])
