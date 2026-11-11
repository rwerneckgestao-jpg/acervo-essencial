# Gera todas as páginas HTML da loja Acervo Essencial a partir de _fonte/catalogo.py.
# Uso: python3 _fonte/gerar.py   (rode na raiz do repositório; não precisa de internet)
import html, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
from catalogo import PRODUTOS, CATEGORIAS, PERFIS, OBJETIVOS, PUBLICOS
from paginas_texto import POLITICA, TERMOS, SOBRE, CREDITOS_FOTOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://rwerneckgestao-jpg.github.io/acervo-essencial/"
VERSAO = "v07"
WHATS = "5562993375885"
WHATS_TXT = "(62) 99337-5885"
EMAIL = "r.werneckgestao@gmail.com"
FACEBOOK = "https://www.facebook.com/profile.php?id=61595753879995"
GAL = json.load(open(os.path.join(RAIZ, "_fonte/galerias.json")))
P = {p["id"]: p for p in PRODUTOS}
C = {c["slug"]: c for c in CATEGORIAS}
e = html.escape

def norm(t):
    return unicodedata.normalize("NFD", t.lower()).encode("ascii", "ignore").decode()

def reais(v):
    if v == 0: return "Grátis"
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s

def foto(nome, peq=False):
    return f"img/fotos/{nome}{'-p' if peq else ''}.jpg"

def galeria(p):
    g = p["galeria"]
    if isinstance(g, str):
        g = [tuple(x) for x in GAL[g]]
    return g

def idade_txt(p):
    if not p.get("idade"): return None
    a, b = p["idade"]
    return f"{a} a {b} anos"

def faixas(p):
    if not p.get("idade"): return []
    a, b = p["idade"]; r = []
    if a <= 5 and b >= 3: r.append("3a5")
    if a <= 8 and b >= 6: r.append("6a8")
    if b >= 9: r.append("9mais")
    return r

FAIXAS = {"3a5": "3 a 5 anos", "6a8": "6 a 8 anos", "9mais": "9 anos ou mais"}

# ---------- ícones (SVG próprios, traço simples) ----------
def ic(nome, cls="ico"):
    d = {
      "busca": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
      "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
      "x": '<path d="M6 6l12 12M18 6L6 18"/>',
      "seta": '<path d="M5 12h14M13 6l6 6-6 6"/>',
      "baixo": '<path d="M6 9l6 6 6-6"/>',
      "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
      "pdf": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 13h6M10 17h4"/>',
      "impressora": '<path d="M7 9V4h10v5"/><rect x="4" y="9" width="16" height="8" rx="2"/><path d="M7 14h10v6H7z"/>',
      "escudo": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
      "cadeado": '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/>',
      "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
      "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
      "alvo": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
      "camadas": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
      "mao": '<path d="M8 13V6a1.5 1.5 0 013 0v5M11 11V4.5a1.5 1.5 0 013 0V11M14 11V6a1.5 1.5 0 013 0v7c0 4-2.5 7-6 7-2.5 0-4-1.2-5.5-3.5L4 13.5a1.5 1.5 0 012.5-1.6L8 14"/>',
      "livro": '<path d="M12 6c-2-1.5-5-2-8-2v14c3 0 6 .5 8 2 2-1.5 5-2 8-2V4c-3 0-6 .5-8 2z"/><path d="M12 6v14"/>',
      "estrela": '<path d="M12 4l2.3 4.8 5.2.7-3.8 3.6.9 5.2L12 15.8 7.4 18.3l.9-5.2L4.5 9.5l5.2-.7z"/>',
      "licenca": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
      "familia": '<circle cx="8" cy="7" r="3"/><circle cx="17" cy="9" r="2.3"/><path d="M3 20c0-3.5 2.2-6 5-6s5 2.5 5 6"/><path d="M13.5 20c0-2.6 1.6-4.6 3.5-4.6S20.5 17.4 20.5 20"/>',
      "quadro": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20l4-4 4 4"/><path d="M7 9h6M7 12h4"/>',
      "fala": '<path d="M4 6h12v8H9l-4 3v-3H4z"/><path d="M19 9c1 1 1.5 2 1.5 3.5S20 15 19 16"/>',
      "coracao": '<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z"/>',
      "predio": '<path d="M4 21V8l8-5 8 5v13"/><path d="M9 21v-6h6v6"/><path d="M8 10h2M14 10h2"/>',
      "play": '<path d="M7 5l12 7-12 7z"/>',
      "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
      "relogio": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
      "facebook": '<path d="M14 8h3V4h-3c-2.8 0-4 1.8-4 4.3V11H7v4h3v6h4v-6h3l1-4h-4V8.6c0-.4.3-.6.7-.6z"/>',
      "whats": '<path d="M5 19l1.2-3.6A7.5 7.5 0 1112 19.5a7.6 7.6 0 01-3.5-.9z"/><path d="M9.5 9.5c.3 1.6 1.6 3.3 3.5 4l1-1 1.5.8c-.3 1-1 1.5-2 1.5-2.8-.2-5-2.6-5.2-5.2 0-1 .6-1.7 1.5-2l.8 1.5z"/>',
      "presente": '<rect x="4" y="9" width="16" height="11" rx="1"/><path d="M3 9h18v-3H3zM12 6v14"/><path d="M12 6c-1.5-3-5-3-5-1s3 1 5 1c2 0 5 1 5-1s-3.5-2-5 1z"/>',
      "tamanho": '<path d="M4 8V4h4M20 8V4h-4M4 16v4h4M20 16v4h-4"/>',
    }[nome]
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'

LOGO = ('<svg viewBox="0 0 120 120" aria-hidden="true"><rect width="120" height="120" rx="24" fill="#F8F3EA"/>'
        '<path d="M60 8 Q62.2 19.8 74 22 Q62.2 24.2 60 36 Q57.8 24.2 46 22 Q57.8 19.8 60 8 Z" fill="#E9B04B"/>'
        '<path d="M58 46 C45 38 30 36 14 38 L14 96 C30 94 45 96 58 104 Z" fill="#174A5E"/>'
        '<path d="M62 46 C75 38 90 36 106 38 L106 96 C90 94 75 96 62 104 Z" fill="#CF5D37"/>'
        '<path d="M24 56 C33 55 41 57 48 61 M24 70 C33 69 41 71 48 75" stroke="#F8F3EA" stroke-width="4" stroke-linecap="round" fill="none"/>'
        '<circle cx="84" cy="68" r="10" fill="#F8F3EA"/></svg>')

def marca(extra=""):
    return f'<a class="marca" href="index.html" aria-label="Acervo Essencial, página inicial">{LOGO}<span><b>Acervo Essencial</b><small>materiais educativos e inclusivos</small></span></a>'

# ---------- cabeça, topo e rodapé ----------
def cabeca(titulo, descricao, caminho, imagem, extra_head="", tipo="website"):
    url = BASE + ("" if caminho == "index.html" else caminho)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descricao)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#174A5E">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="{tipo}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Acervo Essencial">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{imagem}">
<meta name="twitter:card" content="summary_large_image">
<script src="pixel.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Source+Sans+3:wght@400;600&family=Fredoka:wght@600&display=swap">
<link rel="stylesheet" href="loja/estilo.css?{VERSAO}">
{extra_head}</head>
'''

def contar(cat):
    return sum(1 for p in PRODUTOS if cat["slug"] in p["categorias"])

def topo():
    cats = "".join(f'<a href="{c["arquivo"]}.html"><img src="{foto(FOTO_CAT[c["slug"]], True)}" alt="" loading="lazy"><div><b>{e(c["nome"])}</b><span>{contar(c)} {"material" if contar(c) == 1 else "materiais"}</span></div></a>' for c in CATEGORIAS)
    perfis = "".join(f'<a href="{pf["arquivo"]}.html"><img src="{foto(pf["foto"], True)}" alt="" loading="lazy"><div><b>{e(pf["nome"])}</b><span>{len(pf["produtos"])} materiais indicados</span></div></a>' for pf in PERFIS)
    gav_cats = "".join(f'<a href="{c["arquivo"]}.html">{e(c["nome"])} <small>{contar(c)}</small></a>' for c in CATEGORIAS)
    gav_perfis = "".join(f'<a href="{pf["arquivo"]}.html">{e(pf["nome"])}</a>' for pf in PERFIS)
    return f'''<body>
<a class="sr" href="#conteudo">Ir para o conteúdo</a>
<div class="faixa">Materiais digitais em PDF · <b>acesso por e-mail</b> logo após o pagamento · 7 dias de garantia</div>
<header class="topo">
  <div class="envoltorio">
    {marca()}
    <nav class="menu" aria-label="Principal">
      <a href="loja.html">Loja</a>
      <div class="sub"><button type="button" aria-expanded="false">Categorias {ic("baixo", "")}</button><div class="painel">{cats}<a class="todos" href="loja.html">Ver todos os materiais</a></div></div>
      <div class="sub"><button type="button" aria-expanded="false">Para você {ic("baixo", "")}</button><div class="painel">{perfis}</div></div>
      <a href="kits-terapeuticos.html">Kits terapêuticos</a>
      <a href="index.html#amostra">Amostra grátis</a>
    </nav>
    <div class="acoes-topo">
      <button class="icone-btn" type="button" data-abre-busca aria-label="Buscar materiais">{ic("busca", "")}</button>
      <a class="icone-btn" href="ajuda.html" aria-label="Atendimento e ajuda">{ic("chat", "")}</a>
      <button class="icone-btn so-celular" type="button" data-abre-menu aria-label="Abrir menu">{ic("menu", "")}</button>
    </div>
  </div>
</header>
<div class="gaveta" role="dialog" aria-label="Menu">
  <div class="fundo" data-fecha-menu></div>
  <nav>
    <button class="icone-btn fecha" type="button" data-fecha-menu aria-label="Fechar menu">{ic("x", "")}</button>
    <h4>Loja</h4><a href="loja.html">Todos os materiais</a><a href="kits-terapeuticos.html">Kits terapêuticos</a><a href="kit-completo.html">Kit Completo dos cadernos</a><a href="index.html#amostra">Amostra grátis</a>
    <h4>Categorias</h4>{gav_cats}
    <h4>Para você</h4>{gav_perfis}
    <h4>Atendimento</h4><a href="ajuda.html">Ajuda e perguntas</a><a href="https://wa.me/{WHATS}" target="_blank" rel="noopener">WhatsApp {WHATS_TXT}</a>
  </nav>
</div>
<div class="busca" role="dialog" aria-label="Buscar materiais">
  <div class="caixa">
    <div class="campo">{ic("busca")}<label class="sr" for="campo-busca">Buscar</label><input id="campo-busca" type="search" placeholder="Busque por tema, idade ou material" autocomplete="off"><button class="icone-btn" type="button" data-fecha-busca aria-label="Fechar busca">{ic("x", "")}</button></div>
    <div class="resultados" aria-live="polite"></div>
    <div class="sugestoes"><button type="button">rotina</button><button type="button">fala</button><button type="button">alfabetização</button><button type="button">emoções</button><button type="button">autismo</button><button type="button">bingo</button><button type="button">comunicação alternativa</button></div>
  </div>
</div>
<main id="conteudo">
'''

def rodape(scripts=""):
    cats = "".join(f'<li><a href="{c["arquivo"]}.html">{e(c["nome"])}</a></li>' for c in CATEGORIAS)
    perfis = "".join(f'<li><a href="{pf["arquivo"]}.html">{e(pf["titulo"].replace("Para ", "").capitalize())}</a></li>' for pf in PERFIS)
    return f'''</main>
<footer class="rodape">
  <div class="envoltorio">
    <div class="colunas">
      <div>
        {marca()}
        <p style="margin-top:18px;max-width:340px">Materiais educativos e recursos inclusivos organizados por objetivo, com orientação para o adulto, para usar em casa, na escola e nos atendimentos.</p>
        <div class="redes"><a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Acervo Essencial no Facebook">{ic("facebook", "")}</a><a href="https://wa.me/{WHATS}" target="_blank" rel="noopener" aria-label="WhatsApp do Acervo Essencial">{ic("whats", "")}</a></div>
      </div>
      <div><h4>Categorias</h4><ul>{cats}</ul></div>
      <div><h4>Para você</h4><ul>{perfis}</ul></div>
      <div><h4>Atendimento</h4><ul><li><a href="ajuda.html">Central de ajuda</a></li><li><a href="ajuda.html#receber">Como recebo o material</a></li><li><a href="https://wa.me/{WHATS}" target="_blank" rel="noopener">WhatsApp {WHATS_TXT}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
      <div><h4>Institucional</h4><ul><li><a href="sobre.html">Sobre o Acervo Essencial</a></li><li><a href="termos-de-uso.html#licenca">Licença de uso</a></li><li><a href="termos-de-uso.html">Termos e condições</a></li><li><a href="politica-de-privacidade.html">Política de privacidade</a></li><li><a href="creditos.html">Créditos de imagens</a></li></ul></div>
    </div>
    <div class="legal">
      <span>Acervo Essencial · materiais digitais para imprimir e usar. Pagamento processado e arquivos entregues pela Eduzz.</span>
      <span>As imagens de produto mostram páginas reais dos materiais. Fotos e vídeos de pessoas são de banco de imagens (Pexels) e ilustram situações de uso: não são clientes nem profissionais do Acervo Essencial.</span>
      <span>Os materiais são de apoio pedagógico e terapêutico: não fazem diagnóstico e não substituem o acompanhamento profissional. Este site usa o Pixel da Meta (cookies) para medir visitas e anúncios, como explica a política de privacidade.</span>
    </div>
  </div>
</footer>
<script src="loja/catalogo.js?{VERSAO}"></script>
<script src="checkout.js?{VERSAO}"></script>
<script src="loja/loja.js?{VERSAO}"></script>
{scripts}</body>
</html>
'''

# fotos de cada categoria (nome do arquivo em img/fotos sem extensão)
FOTO_CAT = {"educacao": "professora_a", "autismo": "autismo_a", "inclusao": "inclusao_a", "desenvolvimento": "desenvolvimento_a",
            "emocoes": "emocoes_a", "fono": "terapia_b", "jogos": "jogo_a"}

# ---------- card de produto ----------
def etiquetas(p):
    r = []
    if p["tipo"] == "app": r.append(f'<span class="etq app">{ic("tamanho", "")}Digital · app</span>')
    else: r.append(f'<span class="etq digital">{ic("pdf", "")}Digital · PDF</span>')
    if p.get("de"): r.append('<span class="etq combo">Combo</span>')
    return "".join(r)

def card(p, ordem=0):
    cats = " ".join(p["categorias"]); objs = " ".join(p["objetivos"]); pubs = " ".join(p["publicos"])
    busca = norm(" ".join([p["nome"], p["resumo"], p["linha"]] + [OBJETIVOS[o] for o in p["objetivos"]] + [C[c]["nome"] for c in p["categorias"]] + [PUBLICOS[x] for x in p["publicos"]]))
    fich = []
    if idade_txt(p): fich.append(idade_txt(p))
    fich.append(OBJETIVOS[p["objetivos"][0]] if len(p["objetivos"]) == 1 else f'{len(p["objetivos"])} objetivos')
    fich.append(f'{p["paginas"]} páginas' if p["tipo"] != "app" else "92 datas")
    preco = reais(p["preco"])
    sub = f'<small>Separados: {reais(p["de"])}</small>' if p.get("de") else ('<small>ou PDF grátis</small>' if p.get("gratis") else '<small>Pagamento único</small>')
    return f'''<article class="card" data-cat="{cats}" data-obj="{objs}" data-pub="{pubs}" data-idade="{' '.join(faixas(p))}" data-formato="{'app' if p['tipo'] == 'app' else 'pdf'}" data-preco="{p['preco']}" data-nome="{e(p['nome'])}" data-ordem="{ordem}" data-busca="{e(busca)}">
  <a class="foto" href="{p['slug']}.html" tabindex="-1" aria-hidden="true"><img src="img/loja/card_{p['id']}.jpg" alt="" loading="lazy" width="800" height="1000"></a>
  <div class="selo">{etiquetas(p)}</div>
  <div class="corpo">
    <div class="linha">{e(p['linha'])}</div>
    <h3><a href="{p['slug']}.html">{e(p['nome'])}</a></h3>
    <p class="resumo">{e(p['resumo'])}</p>
    <ul class="fichas">{''.join(f'<li>{e(x)}</li>' for x in fich)}</ul>
    <div class="rodape-card"><div class="preco">{preco}{sub}</div><span class="ver"><span>Conhecer</span>{ic("seta", "")}</span></div>
  </div>
</article>'''

def grade(ids, cls="grade"):
    return f'<div class="{cls}">' + "".join(card(P[i], n) for n, i in enumerate(ids)) + "</div>"

# ---------- página inicial ----------
def pagina_inicial():
    tiles = "".join(f'''<a class="tile surge" href="{c['arquivo']}.html"><img src="{foto(FOTO_CAT[c['slug']], i > 1)}" alt="" loading="lazy"><div class="rotulo"><h3>{e(c['nome'])}</h3><span>{contar(c)} {"material" if contar(c) == 1 else "materiais"}{" · jogos para imprimir" if c['slug'] == 'jogos' else ""} {ic("seta", "")}</span></div></a>''' for i, c in enumerate(CATEGORIAS))
    icones_perfil = {"familia": "familia", "professora": "quadro", "fono": "fala", "terapeuta": "coracao", "escola": "predio"}
    abas = "".join(f'<button class="aba" type="button" role="tab" id="aba-{pf["slug"]}" aria-controls="painel-{pf["slug"]}" aria-selected="{"true" if i == 0 else "false"}">{ic(icones_perfil[pf["slug"]])}{e(pf["nome"])}</button>' for i, pf in enumerate(PERFIS))
    paineis = "".join(f'''<div role="tabpanel" id="painel-{pf['slug']}" aria-labelledby="aba-{pf['slug']}"{'' if i == 0 else ' hidden'}>
      <p class="intro">{e(pf['intro'])}</p>
      {grade(pf['produtos'][:3], 'mini-grade')}
      <a class="btn btn-linha" href="{pf['arquivo']}.html">Ver tudo para {e(pf['titulo'].replace('Para ', ''))} {ic("seta", "")}</a>
    </div>''' for i, pf in enumerate(PERFIS))
    destaques = ["kit", "colecao", "p06", "t03", "p01", "b05", "t04", "p02"]
    videos = [
      ("pessoas_mae", "Em casa", "Mãe e filha numa atividade de papel à mesa", True),
      ("p01", "Por dentro: Brincando com os Sons", "Páginas reais do caderno", False),
      ("pessoas_professora", "Na escola", "Professora trabalhando com um pequeno grupo", True),
      ("pessoas_jogo", "Jogar e aprender", "Criança e adulto montando um jogo à mesa", True),
      ("t03", "Por dentro: Comunica", "Pranchas e cartões reais do kit", False),
      ("pessoas_terapia", "No atendimento", "Profissional em sessão com uma criança", True),
    ]
    vids = ""
    for i, (arq, tit, desc, pessoas) in enumerate(videos):
        largo = "" if pessoas else " pagina"
        rot = "Cena ilustrativa · banco de imagens" if pessoas else "Vídeo demonstrativo · páginas reais"
        vids += f'''<figure class="video surge{largo}"><video data-auto muted loop playsinline preload="none" poster="video/{arq}.jpg"><source src="video/{arq}.mp4" type="video/mp4"></video><button class="play" type="button" data-play></button><figcaption><b>{e(tit)}</b><span>{rot}<i class="desc"> · {e(desc)}</i></span></figcaption></figure>'''
    difs = [("alvo", "Organizados por objetivo", "Cada material treina uma habilidade, em ordem, do mais fácil ao mais difícil."),
      ("camadas", "Para diferentes necessidades", "Leitura, fala, atenção, comunicação alternativa, rotina e emoções."),
      ("mao", "Fácil de usar", "Uma página de orientação e o resto é prática pronta: imprimir, recortar e usar."),
      ("email", "Acesso logo após a compra", "A Eduzz envia o link do PDF para o seu e-mail assim que o pagamento é confirmado."),
      ("livro", "Orientação para o adulto", "Guias que explicam o que fazer, como reagir aos erros e quando procurar um profissional."),
      ("estrela", "Cuidado em cada página", "Ilustrações próprias nos kits, revisão de português e páginas testadas na impressão."),
      ("licenca", "Licença transparente", "Imprima quantas vezes quiser para seus filhos, alunos ou pacientes. Só não pode revender.")]
    difs_html = "".join(f'<li>{ic(i)}<div><b>{e(t)}</b><span>{e(d)}</span></div></li>' for i, t, d in difs)
    kit, col, bingo, cal = P["kit"], P["colecao"], P["b05"], P["cal27"]
    faq = [("Como recebo meu material?", "Depois da confirmação do pagamento, a Eduzz envia para o e-mail informado na compra o link para baixar o PDF. Cartão e Pix costumam ser confirmados em minutos; boleto pode levar até 3 dias úteis."),
      ("É produto físico ou digital?", "Hoje todos os materiais do Acervo Essencial são digitais: arquivos em PDF para imprimir e, no caso do Calendário 2027, uma página que abre no navegador. Nada é enviado pelo correio."),
      ("Posso imprimir?", "Sim, quantas vezes quiser, em papel A4 comum, em casa, na escola ou numa gráfica rápida."),
      ("Posso utilizar em sala de aula?", "Sim. A licença permite imprimir para usar com os seus próprios alunos, inclusive mandando a folha impressa para casa. Não é permitido enviar o arquivo PDF para outras professoras ou escolas."),
      ("Posso utilizar em atendimento?", "Sim. Fonoaudiólogos, psicólogos, psicopedagogos e terapeutas podem imprimir para usar com os seus pacientes. Cada profissional que usa o arquivo precisa da sua própria compra."),
      ("Como funciona o pagamento?", "O pagamento é feito na página segura da Eduzz, plataforma que processa a compra. As formas de pagamento disponíveis aparecem na própria página da Eduzz. Você tem 7 dias para desistir e receber o valor de volta."),
      ("Como recebo suporte?", f"Pelo WhatsApp {WHATS_TXT}, em horário comercial, ou pelo e-mail {EMAIL}. Dúvidas de pagamento e reembolso também podem ser resolvidas na área de compras da Eduzz.")]
    faq_html = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    corpo = f'''
<section class="hero-split">
  <div class="envoltorio">
    <div class="texto">
      <p class="sobretitulo">Materiais educativos e recursos inclusivos</p>
      <h1>Cada descoberta começa com uma oportunidade de aprender.</h1>
      <p class="intro">Materiais educativos, recursos inclusivos e atividades cuidadosamente organizadas para apoiar o desenvolvimento infantil em casa, na escola e nos atendimentos.</p>
      <div class="botoes">
        <a class="btn btn-acao" href="loja.html">Explorar coleções {ic("seta", "")}</a>
        <a class="btn btn-linha" href="#caminhos">Encontrar materiais para minha necessidade</a>
      </div>
      <ul class="hero-fatos"><li><b>13</b> materiais à venda</li><li><b>R$ 9,90</b> a partir de</li><li><b>7 dias</b> de garantia</li></ul>
    </div>
    <div class="hero-foto">
      <img src="{foto('hero_b')}" alt="Mãe e filha fazendo uma atividade de papel juntas à mesa" width="1600" height="1067" fetchpriority="high">
      <figure class="hero-pagina"><img src="img/pg/p1-15.jpg" alt="Página real do caderno Brincando com os Sons: atividade Qual rima?" loading="lazy"><figcaption>Página real · Brincando com os Sons</figcaption></figure>
      <span class="credito">Foto ilustrativa</span>
    </div>
  </div>
</section>
<section class="garantias" aria-label="Como funciona a compra">
  <div class="envoltorio"><ul>
    <li>{ic("pdf")}<div><b>Material digital</b>PDF enviado por e-mail</div></li>
    <li>{ic("impressora")}<div><b>Imprima à vontade</b>quantas vezes precisar</div></li>
    <li>{ic("cadeado")}<div><b>Pagamento seguro</b>processado pela Eduzz</div></li>
    <li>{ic("escudo")}<div><b>7 dias de garantia</b>dinheiro de volta</div></li>
  </ul></div>
</section>

<section class="secao" id="caminhos">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Escolha seu caminho</p><h2>Encontre o material pela necessidade da criança</h2><p class="intro">Sete áreas, cada uma com materiais organizados por objetivo. Nenhum material aparece numa área sem ter relação com ela.</p></div><a class="link-seta" href="loja.html">Ver todos os materiais {ic("seta", "")}</a></div>
    <div class="mosaico">{tiles}</div>
  </div>
</section>

<section class="secao creme" id="perfis">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Compre por perfil</p><h2>Quem vai usar o material?</h2></div></div>
    <div class="perfis" data-abas><div class="abas" role="tablist" aria-label="Perfis">{abas}</div><div class="conteudo">{paineis}</div></div>
  </div>
</section>

<section class="secao" id="destaques">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Destaques do acervo</p><h2>Os materiais mais completos da loja</h2><p class="intro">Toque num material para ver as páginas por dentro, para quem é indicado e como usar.</p></div><a class="link-seta" href="loja.html">Ver os 13 materiais {ic("seta", "")}</a></div>
    {grade(destaques)}
  </div>
</section>

<section class="secao escura" id="videos">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Conheça nossos materiais</p><h2>Como os materiais entram na rotina</h2><p class="intro" style="color:#C9D8DC">Em casa, na sala de aula e no atendimento: atividades curtas, no papel, com o adulto do lado.</p></div></div>
    <div class="videos">{vids}</div>
    <p class="aviso-video">Os vídeos com pessoas são cenas ilustrativas de banco de imagens (Pexels) e não mostram clientes nem profissionais do Acervo Essencial. Os vídeos marcados como demonstrativos mostram as páginas reais dos materiais.</p>
  </div>
</section>

<section class="secao" id="porque">
  <div class="envoltorio dupla">
    <div class="foto-grande surge"><img src="{foto('recorte_a')}" alt="Criança recortando papel colorido à mesa" loading="lazy"></div>
    <div class="surge">
      <p class="sobretitulo">Por que escolher o Acervo Essencial</p>
      <h2>Menos busca por folhinhas soltas. Mais tempo com a criança.</h2>
      <ul class="lista-dif">{difs_html}</ul>
    </div>
  </div>
</section>

<section class="secao escura" id="marca">
  <div class="envoltorio dupla">
    <div class="surge">
      <p class="sobretitulo">Conheça nossa marca</p>
      <h2>Um acervo pensado para quem ensina e cuida</h2>
      <p>O Acervo Essencial reúne materiais de apoio para famílias, professoras e profissionais que acompanham o desenvolvimento das crianças. Cada material nasce de uma pergunta prática: o que essa pessoa precisa ter em mãos amanhã, para a próxima atividade, a próxima aula ou a próxima sessão?</p>
      <p>Por isso os materiais vêm prontos, em ordem e com orientação clara. E por isso falamos com honestidade sobre o que eles fazem: são apoio, não diagnóstico nem tratamento.</p>
      <div class="compromissos">
        <div><b>Inclusão de verdade</b><span>Recursos visuais, comunicação alternativa e jogos com adaptações para todas as crianças participarem.</span></div>
        <div><b>Base em pesquisa</b><span>Os guias citam as fontes e dizem com clareza o que a pesquisa mostra e o que ela não garante.</span></div>
        <div><b>Transparência</b><span>Você vê as páginas reais antes de comprar e sabe exatamente o que pode fazer com o arquivo.</span></div>
      </div>
      <a class="btn btn-claro" href="sobre.html" style="margin-top:28px">Conhecer o Acervo Essencial {ic("seta", "")}</a>
    </div>
    <div class="foto-grande surge"><img src="{foto('marca_a')}" alt="Mesa com folhas, lápis de cor, tesoura e cola" loading="lazy"></div>
  </div>
</section>

<section class="secao creme" id="ofertas">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Destaques e ofertas</p><h2>Coleções, kits e materiais avulsos</h2><p class="intro">Os combos saem mais em conta do que os materiais comprados separados. Os valores abaixo são os preços reais de cada item.</p></div></div>
    <div class="ofertas">
      <article class="oferta grande surge">
        <div class="img"><img src="{kit['mesa']}" alt="As páginas dos 4 cadernos do Kit Completo sobre a mesa" loading="lazy"></div>
        <div class="txt">
          <span class="etq combo">Kit de cadernos · 4 em 1</span>
          <h3>Kit Completo: os 4 cadernos</h3>
          <p>Brincando com os Sons, Letras que Viram Palavras, Cobra e Abelha e Olhos Atentos. 173 páginas para crianças de 4 a 7 anos.</p>
          <div class="valores"><span class="preco">{reais(kit['preco'])}</span><s>{reais(kit['de'])}</s><span class="economia">Economia de {reais(kit['de'] - kit['preco'])} sobre os 4 avulsos</span></div>
          <div class="btns"><a class="btn btn-acao" href="kit-completo.html">Conhecer o Kit Completo {ic("seta", "")}</a></div>
        </div>
      </article>
      <article class="oferta surge">
        <div class="img"><img src="img/loja/card_colecao.jpg" alt="Capas dos 4 kits terapêuticos" loading="lazy"></div>
        <div class="txt">
          <span class="etq combo">Coleção · 4 kits</span>
          <h3>Coleção Kits Terapêuticos</h3>
          <p>Fala, motricidade orofacial, comunicação alternativa e emoções.</p>
          <div class="valores"><span class="preco">{reais(col['preco'])}</span><s>{reais(col['de'])}</s></div>
          <div class="btns"><a class="btn btn-marca btn-peq" href="kits-terapeuticos.html">Ver a coleção</a></div>
        </div>
      </article>
      <article class="oferta surge">
        <div class="img"><img src="img/loja/card_b05.jpg" alt="Cartelas do Bingo dos Sons" loading="lazy"></div>
        <div class="txt">
          <span class="etq">Jogo para imprimir</span>
          <h3>Bingo dos Sons</h3>
          <p>3 bingos e 96 cartelas para jogar com a turma toda.</p>
          <div class="valores"><span class="preco">{reais(bingo['preco'])}</span></div>
          <div class="btns"><a class="btn btn-marca btn-peq" href="bingo-dos-sons.html">Ver o Bingo</a><a class="btn btn-linha btn-peq" href="calendario-2027.html">Calendário 2027 grátis</a></div>
        </div>
      </article>
    </div>

    <div class="amostra surge" id="amostra">
      <div>
        <p class="sobretitulo">Amostra grátis, sem cadastro</p>
        <h2>Experimente antes: 16 páginas do Brincando com os Sons</h2>
        <p>O guia do adulto completo, uma atividade de cada etapa e 10 brincadeiras sem papel. Faça hoje com a criança e veja se o formato funciona para vocês.</p>
        <div class="btns" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:22px"><a class="btn btn-acao" href="amostra_gratis_P01.pdf" target="_blank" rel="noopener">{ic("pdf", "")} Baixar a amostra (PDF)</a><a class="btn btn-claro" href="brincando-com-os-sons.html">Ver o caderno completo</a></div>
        <p style="font-size:14px;color:#B9CDD3;margin-top:14px">Pode imprimir e compartilhar a amostra, sem alterações.</p>
      </div>
      <div class="capa-amostra"><img src="amostra_capa_v03.png" alt="Capa da amostra grátis do Brincando com os Sons" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="secao" id="perguntas">
  <div class="envoltorio">
    <div class="cabeca-secao surge" style="justify-content:center;text-align:center"><div><p class="sobretitulo">Perguntas frequentes</p><h2>Antes de comprar</h2></div></div>
    <div class="faq">{faq_html}</div>
    <p style="text-align:center;margin-top:30px"><a class="link-seta" href="ajuda.html">Mais respostas na central de ajuda {ic("seta", "")}</a></p>
  </div>
</section>
'''
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Acervo Essencial", "url": BASE, "logo": BASE + "apple-touch-icon.png",
          "sameAs": [FACEBOOK], "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": EMAIL, "telephone": "+55-62-99337-5885", "availableLanguage": "Portuguese"}}
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    return (cabeca("Acervo Essencial · materiais educativos e recursos inclusivos para imprimir",
                   "Materiais educativos e recursos inclusivos para casa, escola e atendimento: alfabetização, fala, comunicação alternativa, rotina visual e emoções. PDF para imprimir, com orientação para o adulto.",
                   "index.html", "img/loja/og_kit.jpg", extra) + topo() + corpo + rodape())

# ---------- loja (catálogo completo com filtros) ----------
def caixas(nome, opcoes, contagens):
    return "".join(f'<label><input type="checkbox" name="{nome}" value="{v}"> {e(t)} <small>{contagens.get(v, 0)}</small></label>' for v, t in opcoes)

def pagina_loja():
    ordem = ["kit", "colecao", "p01", "p02", "p03", "p04", "b05", "p06", "t01", "t02", "t03", "t04", "cal27"]
    def conta(campo, fn):
        d = {}
        for p in PRODUTOS:
            for v in fn(p): d[v] = d.get(v, 0) + 1
        return d
    filtros = f'''<aside class="filtros" aria-label="Filtros">
      <div class="fechar-filtros" style="display:none;justify-content:space-between;align-items:center;margin-bottom:16px"><b style="font-size:20px">Filtrar</b><button class="icone-btn" type="button" data-fecha-filtros aria-label="Fechar filtros">{ic("x", "")}</button></div>
      <fieldset><legend>Categoria</legend>{caixas("cat", [(c["slug"], c["nome"]) for c in CATEGORIAS], conta("cat", lambda p: p["categorias"]))}</fieldset>
      <fieldset><legend>Objetivo</legend>{caixas("obj", list(OBJETIVOS.items()), conta("obj", lambda p: p["objetivos"]))}</fieldset>
      <fieldset><legend>Para quem</legend>{caixas("pub", list(PUBLICOS.items()), conta("pub", lambda p: p["publicos"]))}</fieldset>
      <fieldset><legend>Idade indicada</legend>{caixas("idade", list(FAIXAS.items()), conta("idade", faixas))}</fieldset>
      <fieldset><legend>Formato</legend>{caixas("formato", [("pdf", "PDF para imprimir"), ("app", "App no navegador")], {"pdf": 12, "app": 1})}</fieldset>
      <button class="btn btn-linha btn-peq" type="button" data-limpa>Limpar filtros</button>
      <button class="btn btn-marca btn-largo so-celular" type="button" data-fecha-filtros style="margin-top:12px">Ver resultados</button>
    </aside>'''
    corpo = f'''
<section class="capa-pagina">
  <img src="{foto('hero_c')}" alt="" >
  <div class="envoltorio">
    <div class="trilha"><a href="index.html">Início</a> / Loja</div>
    <h1>Todos os materiais</h1>
    <p class="intro">Filtre por categoria, objetivo, público ou idade. Todos são digitais: PDF para imprimir ou app no navegador.</p>
  </div>
</section>
<section class="secao" style="padding-top:44px">
  <div class="envoltorio loja" data-filtravel>
    {filtros}
    <div>
      <div class="barra-loja">
        <label class="campo-busca">{ic("busca")}<span class="sr">Buscar na loja</span><input type="search" data-busca-local placeholder="Buscar: rotina, fala, bingo..."></label>
        <button class="btn btn-linha btn-peq so-celular" type="button" data-abre-filtros>Filtrar</button>
        <label><span class="sr">Ordenar</span><select data-ordem><option value="rel">Ordem da loja</option><option value="menor">Menor preço</option><option value="maior">Maior preço</option><option value="az">Nome, de A a Z</option></select></label>
      </div>
      <div class="ativos"></div>
      <p class="contagem"></p>
      <div class="grade tres" data-cards>{"".join(card(P[i], n) for n, i in enumerate(ordem))}</div>
      <div class="nada" hidden><p><b>Nenhum material com esses filtros.</b></p><p>Tire um filtro ou <a href="ajuda.html">fale com a gente</a> e conte o que você procura.</p></div>
    </div>
  </div>
</section>
'''
    return cabeca("Loja · todos os materiais | Acervo Essencial", "Todos os materiais do Acervo Essencial com busca e filtros por categoria, objetivo, público e idade: cadernos, kits terapêuticos, jogos, rotina visual e calendário.", "loja.html", "img/loja/og_kit.jpg") + topo() + corpo + rodape()

# ---------- categoria ----------
def pagina_categoria(c):
    ids = []
    for _, lst in c["subs"]:
        for i in lst:
            if i not in ids: ids.append(i)
    subnav = "".join(f'<a href="#sub-{n}">{e(t)}</a>' for n, (t, _) in enumerate(c["subs"]))
    blocos = "".join(f'<div class="bloco-sub surge" id="sub-{n}"><h2>{e(t)} <small>{len(lst)} {"material" if len(lst) == 1 else "materiais"}</small></h2>{grade(lst, "grade tres")}</div>' for n, (t, lst) in enumerate(c["subs"]))
    objs = "".join(f'<li>{ic("check", "")}{e(o)}</li>' for o in c["objetivos"])
    vazio = f'<div class="nota-honesta surge">{ic("info", "")}<div>{e(c["vazio"])}</div></div>' if c.get("vazio") else ""
    # filtros rápidos por objetivo e idade (só os que existem nesta categoria)
    objs_cat = []
    for i in ids:
        for o in P[i]["objetivos"]:
            if o not in objs_cat: objs_cat.append(o)
    idades = []
    for i in ids:
        for f in faixas(P[i]):
            if f not in idades: idades.append(f)
    chips_o = '<button type="button" data-chip="obj" value="" aria-pressed="true">Todos</button>' + "".join(f'<button type="button" data-chip="obj" value="{o}" aria-pressed="false">{e(OBJETIVOS[o])}</button>' for o in objs_cat)
    chips_i = "".join(f'<button type="button" data-chip="idade" value="{f}" aria-pressed="false">{FAIXAS[f]}</button>' for f in ["3a5", "6a8", "9mais"] if f in idades)
    vid_ids = [i for i in ids if os.path.exists(os.path.join(RAIZ, f"video/{i}.mp4"))][:2]
    vids = "".join(f'<figure class="video surge pagina"><video data-auto muted loop playsinline preload="none" poster="video/{i}.jpg"><source src="video/{i}.mp4" type="video/mp4"></video><button class="play" type="button" data-play></button><figcaption><b>Por dentro: {e(P[i]["curto"])}</b><span>Vídeo demonstrativo · páginas reais</span></figcaption></figure>' for i in vid_ids)
    outras = "".join(f'<a href="{o["arquivo"]}.html">{e(o["nome"])}</a>' for o in CATEGORIAS if o["slug"] != c["slug"])
    corpo = f'''
<section class="capa-pagina">
  <img src="{foto(c['foto'] if c['foto'] != 'terapia' else 'terapia_b') if False else foto(FOTO_CAT[c['slug']])}" alt="">
  <div class="envoltorio">
    <div class="trilha"><a href="index.html">Início</a> / <a href="loja.html">Loja</a> / {e(c['nome'])}</div>
    <p class="sobretitulo" style="color:var(--mostarda)">Categoria · {contar(c)} {"material" if contar(c) == 1 else "materiais"}</p>
    <h1>{e(c['titulo'])}</h1>
    <p class="intro">{e(c['intro'])}</p>
    <ul class="objetivos-cat">{objs}</ul>
  </div>
</section>
<section class="secao" style="padding-top:44px" data-filtravel>
  <div class="envoltorio">
    <div class="subnav">{subnav}</div>
    <div class="chips-filtro" aria-label="Filtrar por objetivo">{chips_o}</div>
    {'<div class="chips-filtro" aria-label="Filtrar por idade" style="margin-top:-12px">' + chips_i + '</div>' if len(chips_i) and len(idades) > 1 else ''}
    {blocos}
    {vazio}
  </div>
</section>
{f'<section class="secao creme"><div class="envoltorio"><div class="cabeca-secao surge"><div><p class="sobretitulo">Veja por dentro</p><h2>Vídeos demonstrativos desta categoria</h2></div></div><div class="videos">{vids}</div></div></section>' if vids else ''}
<section class="secao"><div class="envoltorio"><div class="cabeca-secao"><div><p class="sobretitulo">Outras categorias</p><h2>Continue explorando</h2></div></div><div class="subnav">{outras}<a href="loja.html">Todos os materiais</a></div></div></section>
'''
    return cabeca(f"{c['titulo']} · materiais para imprimir | Acervo Essencial", c["intro"][:300], c["arquivo"] + ".html", f"img/fotos/{FOTO_CAT[c['slug']]}-p.jpg") + topo() + corpo + rodape()

# ---------- perfil ----------
CATS_PERFIL = {"familia": ["educacao", "desenvolvimento", "emocoes"], "professora": ["educacao", "jogos", "inclusao"], "fono": ["fono", "desenvolvimento", "autismo"],
               "terapeuta": ["emocoes", "autismo", "educacao"], "escola": ["educacao", "inclusao", "fono"]}
def pagina_perfil(pf):
    cats = "".join(f'<a href="{C[c]["arquivo"]}.html">{e(C[c]["nome"])}</a>' for c in CATS_PERFIL[pf["slug"]])
    corpo = f'''
<section class="capa-pagina">
  <img src="{foto(pf['foto'])}" alt="">
  <div class="envoltorio">
    <div class="trilha"><a href="index.html">Início</a> / Para você / {e(pf['nome'])}</div>
    <p class="sobretitulo" style="color:var(--mostarda)">Compre por perfil</p>
    <h1>{e(pf['titulo'])}</h1>
    <p class="intro">{e(pf['intro'])}</p>
  </div>
</section>
<section class="secao" style="padding-top:44px">
  <div class="envoltorio">
    <div class="nota-honesta surge" style="background:var(--petroleo-claro);border-color:#CFE0E5;color:var(--tinta)">{ic("info", "")}<div><b>Por onde começar:</b> {e(pf['dica'])}</div></div>
    <div class="cabeca-secao" style="margin-top:44px"><div><h2>Materiais indicados</h2><p class="intro">{len(pf['produtos'])} materiais escolhidos para este perfil, do mais procurado para começar ao mais específico.</p></div></div>
    {grade(pf['produtos'], 'grade tres')}
    <div class="cabeca-secao" style="margin-top:60px"><div><h2>Categorias relacionadas</h2></div></div>
    <div class="subnav">{cats}<a href="loja.html">Todos os materiais</a></div>
  </div>
</section>
'''
    corpo = corpo.replace("do mais procurado para começar ao mais específico", "na ordem em que sugerimos conhecer")
    return cabeca(f"{pf['titulo']} | Acervo Essencial", pf["intro"][:300], pf["arquivo"] + ".html", f"img/fotos/{pf['foto']}-p.jpg") + topo() + corpo + rodape()

# ---------- produto ----------
def relacionados(p):
    pontos = []
    for q in PRODUTOS:
        if q["id"] == p["id"]: continue
        s = len(set(q["categorias"]) & set(p["categorias"])) * 2 + len(set(q["objetivos"]) & set(p["objetivos"])) * 3 + len(set(q["publicos"]) & set(p["publicos"]))
        pontos.append((s, q["id"]))
    pontos.sort(key=lambda x: -x[0])
    return [i for _, i in pontos[:4]]

def pagina_produto(p):
    g = galeria(p)
    nome = p["nome"]
    imgs = [(p["capa"], f"{nome}: capa")] + [(a, f"{nome}: {b}") for a, b in g]
    if p.get("capas"):
        imgs = [(f"img/loja/card_{p['id']}.jpg", f"{nome}: capas")] + imgs[1:]
    principal = imgs[0]
    minis = "".join(f'<button type="button" data-img="{a}" data-legenda="{e(b)}"{" aria-current=\"true\"" if n == 0 else ""} aria-label="Ver {e(b)}"><img src="{a}" alt="" loading="lazy"></button>' for n, (a, b) in enumerate(imgs[:9]))
    fr = []
    fr.append(("Idade", idade_txt(p) or ("Adultos" if p["tipo"] == "app" else "Conforme avaliação")))
    fr.append(("Páginas", str(p["paginas"]) if p["tipo"] != "app" else "92 datas"))
    fr.append(("Formato", "App + PDF" if p["tipo"] == "app" else "PDF A4"))
    ficha_rapida = "".join(f'<li>{e(a)}<b>{e(b)}</b></li>' for a, b in fr)
    chave = p["id"]
    if p.get("gratis"):
        botoes = f'''<a class="btn btn-acao btn-largo" href="#" data-checkout="{chave}" data-alvo-barra>Quero a versão interativa · {reais(p['preco'])}</a>
          <a class="btn btn-linha btn-largo" href="#" data-checkout="{p['gratis']}">{ic("pdf", "")} Receber o PDF grátis</a>'''
    else:
        botoes = f'<a class="btn btn-acao btn-largo" href="#" data-checkout="{chave}" data-alvo-barra>Comprar agora · {reais(p["preco"])}</a>'
        if p.get("amostra"):
            botoes += f'<a class="btn btn-linha btn-largo" href="amostra_gratis_P01.pdf" target="_blank" rel="noopener">{ic("pdf", "")} Baixar amostra grátis</a>'
    de = f'<s>{reais(p["de"])}</s>' if p.get("de") else ""
    obs = (f'Comprando separados: {reais(p["de"])}. Economia de {reais(p["de"] - p["preco"])}.' if p.get("de") else
           ("PDF grátis com cadastro na Eduzz, ou versão interativa por R$ 9,90." if p.get("gratis") else "Pagamento único. Sem mensalidade."))
    entrega = "Link enviado por e-mail pela Eduzz; abre no navegador" if p["tipo"] == "app" else "PDF enviado por e-mail pela Eduzz"
    trilho = "".join(f'<button type="button" data-zoom="{a}" data-legenda="{e(nome)} · {e(b)}"><img src="{a}" alt="{e(nome)}: {e(b)}" loading="lazy"><span>{e(b)}</span></button>' for a, b in g)
    murais = ""
    if p.get("todas"):
        legs = {"img/todas_p1.jpg": "Brincando com os Sons · 40 páginas", "img/todas_p2.jpg": "Letras que Viram Palavras · 48 páginas", "img/todas_p3.jpg": "Cobra e Abelha · 42 páginas",
                "img/todas_p4.jpg": "Olhos Atentos · 43 páginas", "img/kits/todas_t01.jpg": "Fala em Foco · 43 páginas", "img/kits/todas_t02.jpg": "Motricidade Orofacial · 33 páginas",
                "img/kits/todas_t03.jpg": "Comunica · 32 páginas", "img/kits/todas_t04.jpg": "Emoções e Regulação · 31 páginas"}
        itens = "".join(f'<button type="button" data-zoom="{t}" data-legenda="{e(legs.get(t, nome + " · todas as páginas"))}"><img src="{t}" alt="Todas as páginas de {e(legs.get(t, nome))}" loading="lazy"><span>{e(legs.get(t, f"{nome} · {p[chr(112)+chr(97)+chr(103)+chr(105)+chr(110)+chr(97)+chr(115)]} páginas"))}</span></button>' for t in p["todas"])
        murais = f'<h3 style="margin-top:44px">{"Todas as páginas, sem tirar nenhuma" if len(p["todas"]) == 1 else "Todas as páginas de cada material"}</h3><div class="mural{" varios" if len(p["todas"]) > 1 else ""}" data-grupo>{itens}</div>'
    tem_video = os.path.exists(os.path.join(RAIZ, f"video/{chave}.mp4"))
    demo = ""
    objetivo_html = f'<p class="sobretitulo">Objetivo</p><h2>Para que serve</h2><p class="intro">{e(p["objetivo"])}</p><ul class="fichas" style="margin-top:18px">' + "".join(f'<li>{e(OBJETIVOS[o])}</li>' for o in p["objetivos"]) + "</ul>"
    if tem_video:
        demo = f'''<section class="secao creme"><div class="envoltorio demo">
  <figure class="surge" style="margin:0"><video data-auto muted loop playsinline preload="none" poster="video/{chave}.jpg" controls><source src="video/{chave}.mp4" type="video/mp4"></video><figcaption class="aviso">Vídeo demonstrativo com páginas reais do material.</figcaption></figure>
  <div class="surge">{objetivo_html}</div></div></section>'''
    else:
        demo = f'<section class="secao creme"><div class="envoltorio" style="max-width:860px">{objetivo_html}</div></section>'
    # itens inclusos (kit e coleção)
    inclusos = ""
    if p["id"] == "kit": inclusos = ["p01", "p02", "p03", "p04"]
    if p["id"] == "colecao": inclusos = ["t01", "t02", "t03", "t04"]
    inclusos_html = f'<section class="secao"><div class="envoltorio"><div class="cabeca-secao"><div><p class="sobretitulo">Incluído no combo</p><h2>Os materiais que vêm juntos</h2></div></div>{grade(inclusos)}</div></section>' if inclusos else ""
    oferece = "".join(f'<li>{ic("check", "")}<span>{e(x)}</span></li>' for x in p["oferece"])
    paraquem = "".join(f'<li>{ic("check", "")}<span>{e(x)}</span></li>' for x in p["paraquem"])
    passos = "".join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in p["comousar"])
    icones_b = ["alvo", "estrela", "mao", "escudo"]
    benef = "".join(f'<li>{ic(icones_b[n % 4], "")}{e(b)}</li>' for n, b in enumerate(p["beneficios"]))
    pesquisa = ""
    if p.get("pesquisa"):
        arts = "".join(f'<article><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a, b in p["pesquisa"])
        pesquisa = f'<section class="secao"><div class="envoltorio"><div class="cabeca-secao"><div><p class="sobretitulo">Base na pesquisa</p><h2>Feito a partir do que os estudos mostram</h2><p class="intro">O guia do material resume essas fontes em linguagem simples. As referências completas estão no arquivo.</p></div></div><div class="pesquisa">{arts}</div><p class="aviso">Os estudos descrevem grupos de crianças. Nenhum material garante um resultado individual.</p></div></section>'
    faq = list(p["faq"]) + [
        ("Como recebo?", "Depois da confirmação do pagamento, a Eduzz envia o link para o e-mail informado na compra." + (" O link abre no navegador do celular ou do computador." if p["tipo"] == "app" else " Você baixa o PDF e imprime em papel A4 comum.")),
        ("Posso usar com a minha turma ou com meus pacientes?", "Sim. Você pode imprimir quantas vezes quiser para usar com seus filhos, alunos ou pacientes. Não pode revender nem enviar o arquivo para outras pessoas."),
        ("Isso substitui um profissional?", "Não. É material de apoio: não faz diagnóstico nem tratamento e não substitui professor, fonoaudiólogo, psicólogo ou outro profissional."),
        ("E se eu não gostar?", "Você tem 7 dias de garantia. Peça o reembolso pela Eduzz ou fale com o atendimento.")]
    vistos = set(); faq_u = []
    for q, a in faq:
        if q in vistos: continue
        vistos.add(q); faq_u.append((q, a))
    faq_html = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq_u)
    cat0 = C[p["categorias"][0]]
    tabela = [("Material", p["linha"]), ("Formato", "Página que abre no navegador, mais PDF de 35 páginas" if p["tipo"] == "app" else f"PDF em A4, {p['paginas']} páginas"),
              ("Conteúdo", p["itens"]), ("Idade indicada", idade_txt(p) or ("Para adultos que planejam aulas e atendimentos" if p["tipo"] == "app" else "Definida pelo profissional, conforme a avaliação de cada criança")),
              ("Entrega", entrega), ("Impressão", "Opcional: o PDF grátis pode ser impresso" if p["tipo"] == "app" else "Em casa, na escola ou em gráfica rápida, quantas vezes precisar"), ("Garantia", "7 dias, com devolução do valor")]
    tabela_html = "".join(f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a, b in tabela)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": nome, "description": p["resumo"], "image": [BASE + f"img/loja/card_{chave}.jpg", BASE + p["capa"]],
          "brand": {"@type": "Brand", "name": "Acervo Essencial"}, "category": p["linha"],
          "offers": {"@type": "Offer", "price": f"{p['preco']:.2f}", "priceCurrency": "BRL", "availability": "https://schema.org/InStock", "url": BASE + p["slug"] + ".html"}}
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    corpo = f'''
<div class="envoltorio"><div class="trilha"><a href="index.html">Início</a> / <a href="{cat0['arquivo']}.html">{e(cat0['nome'])}</a> / {e(nome)}</div></div>
<section class="envoltorio produto-topo" data-produto="{chave}">
  <div class="vitrine" data-grupo>
    <button class="principal" type="button" data-zoom="{principal[0]}" data-legenda="{e(principal[1])}" aria-label="Ampliar imagem"><img src="{principal[0]}" alt="{e(principal[1])}" width="900" height="1125" fetchpriority="high"></button>
    <div class="miniaturas">{minis}</div>
  </div>
  <div class="compra">
    <div class="linha-prod">{etiquetas(p)}<span class="etq">{e(p['linha'])}</span></div>
    <h1>{e(nome)}</h1>
    <p class="resumo">{e(p['resumo'])}</p>
    <ul class="ficha-rapida">{ficha_rapida}</ul>
    <div class="caixa-compra">
      <div class="valor"><span class="preco">{reais(p['preco'])}</span>{de}</div>
      <p class="obs">{e(obs)}</p>
      {botoes}
      <ul class="seguro">
        <li>{ic("email", "")}<span>{e(entrega)}, logo após a confirmação do pagamento</span></li>
        <li>{ic("impressora", "")}<span>{"Use no celular, no tablet ou no computador" if p["tipo"] == "app" else "Imprima quantas vezes precisar, em papel A4 comum"}</span></li>
        <li>{ic("cadeado", "")}<span>Pagamento processado pela Eduzz</span></li>
        <li>{ic("escudo", "")}<span>7 dias de garantia: não gostou, pede o dinheiro de volta</span></li>
      </ul>
    </div>
    <p style="font-size:15px;margin-top:16px;color:var(--tinta-2)">Dúvida antes de comprar? <a href="https://wa.me/{WHATS}?text={e('Olá! Tenho uma dúvida sobre o material ' + nome)}" target="_blank" rel="noopener">Fale no WhatsApp</a>.</p>
  </div>
</section>
<nav class="ancoras" aria-label="Seções do produto"><div class="envoltorio"><a href="#por-dentro">Por dentro</a><a href="#o-que-vem">O que vem</a><a href="#para-quem">Para quem é</a><a href="#como-usar">Como usar</a><a href="#licenca">Licença</a><a href="#perguntas">Perguntas</a></div></nav>
<section class="secao" id="por-dentro">
  <div class="envoltorio">
    <div class="cabeca-secao"><div><p class="sobretitulo">Veja por dentro</p><h2>Páginas reais, do jeito que saem na impressora</h2><p class="intro">Toque numa página para ampliar. Arraste para o lado para ver mais.</p></div>
      <div class="setas" style="display:flex;gap:8px"><button class="icone-btn" type="button" data-rolar="-1" aria-label="Voltar páginas" onclick="this.closest('.secao').querySelector('.trilho').scrollBy({{left:-600,behavior:'smooth'}})">&lsaquo;</button><button class="icone-btn" type="button" aria-label="Avançar páginas" onclick="this.closest('.secao').querySelector('.trilho').scrollBy({{left:600,behavior:'smooth'}})">&rsaquo;</button></div></div>
    <div class="rolo" data-grupo><div class="trilho">{trilho}</div></div>
    {murais}
  </div>
</section>
{demo}
{inclusos_html}
<section class="secao" id="o-que-vem">
  <div class="envoltorio colunas-info">
    <div class="surge"><p class="sobretitulo">O que o material oferece</p><h2>O que você recebe</h2><ul class="lista-check">{oferece}</ul></div>
    <div class="surge"><p class="sobretitulo">Ficha técnica</p><h2>Detalhes</h2><table class="tabela-ficha">{tabela_html}</table></div>
  </div>
</section>
<section class="secao creme" id="para-quem">
  <div class="envoltorio colunas-info">
    <div class="surge"><p class="sobretitulo">Para quem é indicado</p><h2>Quem vai aproveitar</h2><ul class="lista-check">{paraquem}</ul></div>
    <div class="surge"><p class="sobretitulo">Benefícios reais</p><h2>Por que vale a pena</h2><ul class="beneficios" style="grid-template-columns:1fr 1fr">{benef}</ul></div>
  </div>
</section>
<section class="secao" id="como-usar">
  <div class="envoltorio"><div class="cabeca-secao"><div><p class="sobretitulo">Como utilizar</p><h2>Em três passos</h2></div></div><ol class="passos">{passos}</ol></div>
</section>
{pesquisa}
<section class="secao creme" id="licenca">
  <div class="envoltorio">
    <div class="cabeca-secao"><div><p class="sobretitulo">Licença de uso</p><h2>O que você pode fazer com o arquivo</h2></div><a class="link-seta" href="termos-de-uso.html#licenca">Ler os termos completos {ic("seta", "")}</a></div>
    <div class="licenca">
      <div class="sim"><h3>{ic("check", "")}Pode</h3><ul><li>Imprimir quantas vezes quiser</li><li>Usar com seus filhos, alunos ou pacientes</li><li>Mandar a folha impressa para casa</li><li>Plastificar e montar o seu acervo</li></ul></div>
      <div class="nao"><h3>{ic("x", "")}Não pode</h3><ul><li>Revender ou compartilhar o arquivo PDF</li><li>Enviar o arquivo para outras pessoas, grupos ou escolas</li><li>Publicar as páginas na internet</li><li>Alterar o material para distribuir como seu</li></ul></div>
    </div>
  </div>
</section>
<section class="secao" id="perguntas">
  <div class="envoltorio"><div class="cabeca-secao" style="justify-content:center;text-align:center"><div><p class="sobretitulo">Perguntas frequentes</p><h2>Dúvidas sobre o {e(p['curto'])}</h2></div></div><div class="faq">{faq_html}</div></div>
</section>
<section class="secao" style="padding-top:0">
  <div class="envoltorio"><div class="cta-final">
    <p class="sobretitulo">{e(p['linha'])}</p>
    <h2>{e(nome)}</h2>
    <div class="valor">{'<s>' + reais(p['de']) + '</s>' if p.get('de') else ''}{reais(p['preco'])}</div>
    <a class="btn btn-acao" href="#" data-checkout="{chave}">{'Quero a versão interativa' if p.get('gratis') else 'Comprar agora'} {ic("seta", "")}</a>
    <p style="margin:16px 0 0;font-size:14px;color:#B9CDD3">7 dias de garantia · Pagamento pela Eduzz · {"Link" if p["tipo"] == "app" else "PDF"} no seu e-mail</p>
  </div></div>
</section>
<section class="secao creme">
  <div class="envoltorio"><div class="cabeca-secao"><div><p class="sobretitulo">Produtos relacionados</p><h2>Combina com este material</h2></div><a class="link-seta" href="loja.html">Ver todos {ic("seta", "")}</a></div>{grade(relacionados(p))}</div>
</section>
<div class="barra-compra"><div><b>{e(p['curto'])}</b><span class="preco">{reais(p['preco'])}</span></div><a class="btn btn-acao" href="#" data-checkout="{chave}">Comprar</a></div>
'''
    titulo = f"{nome} · {p['linha'].lower()} | Acervo Essencial"
    return cabeca(titulo, p["resumo"], p["slug"] + ".html", f"img/loja/og_{chave}.jpg", extra, "product") + topo() + corpo + rodape()

# ---------- páginas de texto ----------
def pagina_texto(arquivo, titulo, descricao, corpo_html, capa=None):
    topo_html = (f'<section class="capa-pagina"><img src="{foto(capa)}" alt=""><div class="envoltorio"><div class="trilha"><a href="index.html">Início</a> / {e(titulo)}</div><h1>{e(titulo)}</h1></div></section>'
                 if capa else f'<div class="envoltorio"><div class="trilha"><a href="index.html">Início</a> / {e(titulo)}</div></div><div class="envoltorio texto-longo" style="padding-top:30px"><h1 style="font-size:clamp(32px,4vw,46px)">{e(titulo)}</h1></div>')
    corpo = f'{topo_html}<section class="secao" style="padding-top:40px"><div class="envoltorio texto-longo">{corpo_html}</div></section>'
    return cabeca(f"{titulo} | Acervo Essencial", descricao, arquivo, "img/loja/og_kit.jpg") + topo() + corpo + rodape()

def pagina_ajuda():
    faq = [("Como recebo meu material?", "Depois da confirmação do pagamento, a Eduzz envia o link para o e-mail informado na compra. Cartão e Pix costumam ser confirmados em minutos; boleto pode levar até 3 dias úteis. Se não chegar, confira a caixa de spam e as abas Promoções e Atualizações."),
      ("Não recebi o e-mail. E agora?", f"Confira o spam. Se não estiver lá, entre na área de compras da Eduzz com o e-mail usado na compra, ou fale com a gente pelo WhatsApp {WHATS_TXT} ou pelo e-mail {EMAIL}."),
      ("É produto físico ou digital?", "Digital. Os materiais são arquivos em PDF para imprimir e, no Calendário 2027, uma página que abre no navegador. Nada é enviado pelo correio. Se um dia vendermos produtos físicos, eles serão identificados como físicos na loja."),
      ("Preciso de impressora colorida?", "Não é obrigatório. Os cadernos funcionam também em preto e branco. Nos kits com cartões e pranchas, a impressão colorida ajuda a criança a reconhecer as figuras."),
      ("Posso utilizar em sala de aula?", "Sim, com os seus próprios alunos. Não é permitido enviar o arquivo para outras professoras ou para a escola inteira: cada profissional que usa o arquivo precisa da sua compra."),
      ("Posso utilizar em atendimento?", "Sim. Imprima para usar com os seus pacientes e para mandar atividades para casa."),
      ("Sou escola e quero para a equipe toda.", f"A licença é individual. Para compras em quantidade, fale com a gente pelo WhatsApp {WHATS_TXT} antes de comprar."),
      ("Como funciona o pagamento?", "Na página segura da Eduzz, que processa a compra. As formas de pagamento aparecem lá, no momento da compra."),
      ("Como peço reembolso?", "Em até 7 dias depois do pagamento, pela área de compras da Eduzz ou pelo nosso e-mail, sem precisar explicar o motivo, como prevê o art. 49 do Código de Defesa do Consumidor."),
      ("Os materiais substituem um profissional?", "Não. São materiais de apoio. Não fazem diagnóstico e não substituem professor, fonoaudiólogo, psicólogo, psicopedagogo ou terapeuta.")]
    faq_html = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    corpo = f'''
<div class="cartoes-ajuda">
  <div>{ic("whats")}<h3>WhatsApp</h3><p>Atendimento em horário comercial.</p><a class="btn btn-marca btn-peq" href="https://wa.me/{WHATS}" target="_blank" rel="noopener">{WHATS_TXT}</a></div>
  <div>{ic("email")}<h3>E-mail</h3><p>Respondemos em até 2 dias úteis.</p><a class="btn btn-linha btn-peq" href="mailto:{EMAIL}">{EMAIL}</a></div>
  <div id="receber">{ic("pdf")}<h3>Como recebo</h3><p>A Eduzz envia o link do material para o e-mail da compra logo após a confirmação do pagamento.</p></div>
</div>
<h2>Perguntas frequentes</h2>
<div class="faq" style="max-width:none">{faq_html}</div>
'''
    return pagina_texto("ajuda.html", "Central de ajuda", "Como receber o material, licença de uso, pagamento, reembolso e atendimento do Acervo Essencial.", corpo)

def catalogo_js():
    itens = []
    for p in PRODUTOS:
        b = norm(" ".join([p["nome"], p["resumo"], p["linha"], " ".join(p["oferece"])] + [OBJETIVOS[o] for o in p["objetivos"]] + [C[c]["nome"] for c in p["categorias"]] + [PUBLICOS[x] for x in p["publicos"]] + (["autismo tea tdah"] if "autismo" in p["categorias"] else [])))
        itens.append({"id": p["id"], "nome": p["nome"], "linha": p["linha"], "url": p["slug"] + ".html", "img": f"img/loja/card_{p['id']}.jpg", "preco": p["preco"], "idade": idade_txt(p), "busca": b})
    return "// Gerado por _fonte/gerar.py: catálogo para a busca do site.\nwindow.CATALOGO = " + json.dumps(itens, ensure_ascii=False) + ";\n"

def sitemap(arquivos):
    urls = "".join(f"<url><loc>{BASE}{'' if a == 'index.html' else a}</loc></url>" for a in arquivos)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'

def grava(arquivo, conteudo):
    if "—" in conteudo or "–" in conteudo:
        raise SystemExit(f"Travessão encontrado em {arquivo} (regra 7)")
    open(os.path.join(RAIZ, arquivo), "w", encoding="utf-8").write(conteudo)
    return arquivo

if __name__ == "__main__":
    feitos = [grava("index.html", pagina_inicial()), grava("loja.html", pagina_loja())]
    for c in CATEGORIAS: feitos.append(grava(c["arquivo"] + ".html", pagina_categoria(c)))
    for pf in PERFIS: feitos.append(grava(pf["arquivo"] + ".html", pagina_perfil(pf)))
    for p in PRODUTOS: feitos.append(grava(p["slug"] + ".html", pagina_produto(p)))
    feitos.append(grava("ajuda.html", pagina_ajuda()))
    feitos.append(grava("sobre.html", pagina_texto("sobre.html", "Sobre o Acervo Essencial", "Quem somos, o que fazemos e como os materiais do Acervo Essencial são feitos.", SOBRE, "marca_a")))
    feitos.append(grava("politica-de-privacidade.html", pagina_texto("politica-de-privacidade.html", "Política de privacidade", "Como o Acervo Essencial trata dados pessoais, cookies e o Pixel da Meta, conforme a LGPD.", POLITICA)))
    feitos.append(grava("termos-de-uso.html", pagina_texto("termos-de-uso.html", "Termos e condições", "Termos de compra, entrega, licença de uso e garantia dos materiais do Acervo Essencial.", TERMOS)))
    feitos.append(grava("creditos.html", pagina_texto("creditos.html", "Créditos de imagens", "Origem e licença das fotos, vídeos, ilustrações e fontes usadas no site do Acervo Essencial.", CREDITOS_FOTOS)))
    open(os.path.join(RAIZ, "loja/catalogo.js"), "w").write(catalogo_js())
    open(os.path.join(RAIZ, "sitemap.xml"), "w").write(sitemap(feitos))
    open(os.path.join(RAIZ, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    print(len(feitos), "páginas geradas")
