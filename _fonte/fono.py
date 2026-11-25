# Páginas do reposicionamento para fonoaudiólogas (25/11/2026):
# nova página inicial, página de captura do Kit Grátis da Fono e página de confirmação.
# Chamado por gerar.py. Reaproveita cabeça, topo, rodapé, cards e ícones do gerador.
import json
import gerar as g
from gerar import e, ic, reais, P, PRODUTOS, CATEGORIAS, PERFIS, BASE, FACEBOOK, WHATS, WHATS_TXT

KG = "img/kitgratis/"
KIT_URL = "kit-gratis-da-fono.html"

# Páginas reais do Kit Grátis (geradas de KIT_GRATIS_DA_FONO/Kit-Gratis-da-Fono.pdf)
KIT_PAGINAS = [("kg-01.jpg", "Capa"), ("kg-03.jpg", "Ficha de observação dos sons"), ("kg-05.jpg", "Pares mínimos: faca ou vaca"),
               ("kg-07.jpg", "Pares mínimos: dente ou pente"), ("kg-10.jpg", "Cartas de linguagem"), ("kg-12.jpg", "Sugestões de exploração"),
               ("kg-13.jpg", "Anamnese complementar"), ("kg-15.jpg", "Materiais completos")]
KIT_ITENS = [("Ficha de observação dos sons", "2 páginas para registrar o que você observou em cada som, com campo para estimulabilidade. Não é teste padronizado."),
             ("20 cartões de pares mínimos", "10 pares ilustrados para recortar: faca e vaca, pato e gato, mala e bala, lua e rua e outros."),
             ("10 cartas de linguagem", "Nomear, agrupar, explicar e descrever, com resposta de referência e 4 formas de jogar."),
             ("Ficha de anamnese complementar", "2 páginas para completar a anamnese que você já usa: fala no dia a dia, audição, rotina e combinados.")]

# Objetivos com produtos reais do catálogo (só produtos que existem; nada inventado)
OBJ_FONO = [
    ("Fala e articulação", "fala", ["t01", "p03", "b05"], "Sons da fala, pares mínimos, S e Z, consciência fonológica em jogo."),
    ("Linguagem", "linguagem", ["t08", "t03", "t07"], "Vocabulário, categorias, narrativa, comunicação alternativa e linguagem do adulto."),
    ("Motricidade orofacial", "motricidade", ["t02"], "Exercícios em forma de jogo, sopro e registro de evolução."),
    ("Organização profissional", "documentos", ["t06"], "Anamneses, plano terapêutico, evolução, relatórios e documentos do consultório."),
]

def galeria(itens, grupo_legenda):
    return '<div class="rolo" data-grupo><div class="trilho">' + "".join(
        f'<button type="button" data-zoom="{src}" data-legenda="{e(grupo_legenda)} · {e(leg)}"><img src="{src}" alt="{e(grupo_legenda)}: {e(leg)}" loading="lazy"><span>{e(leg)}</span></button>'
        for src, leg in itens) + "</div></div>"

def setas():
    return ('<div class="setas"><button class="icone-btn" type="button" aria-label="Voltar páginas" onclick="this.closest(\'.secao\').querySelector(\'.trilho\').scrollBy({left:-600,behavior:\'smooth\'})">&lsaquo;</button>'
            '<button class="icone-btn" type="button" aria-label="Avançar páginas" onclick="this.closest(\'.secao\').querySelector(\'.trilho\').scrollBy({left:600,behavior:\'smooth\'})">&rsaquo;</button></div>')

def bloco_kit(origem):
    itens = "".join(f'<li><span class="fh-num">{i + 1}</span><div><b>{e(t)}</b><span>{e(d)}</span></div></li>' for i, (t, d) in enumerate(KIT_ITENS))
    return f'''<div class="fh-kit">
  <div class="fh-kit-txt">
    <ul class="fh-lista">{itens}</ul>
    <p class="fh-nota">15 páginas em PDF A4, ilustrações próprias do Acervo. Recurso complementar: a seleção e a adaptação são da fonoaudióloga responsável.</p>
    <a class="btn btn-acao" href="{KIT_URL}?{origem}" data-kit-gratis>Conhecer o Kit Grátis da Fono {ic("seta", "")}</a>
  </div>
  <div class="fh-leque" aria-hidden="true">
    <img src="{KG}kg-05.jpg" alt="" loading="lazy"><img src="{KG}kg-10.jpg" alt="" loading="lazy"><img src="{KG}kg-03.jpg" alt="" loading="lazy">
  </div>
</div>'''

def pagina_inicial():
    n = len(PRODUTOS)
    fono = sum(1 for p in PRODUTOS if "fono" in p["categorias"])
    combo = P["fono3"]
    combo_itens = "".join(f"<li>{e(x)}</li>" for x in combo["oferece"][:3])
    objetivos = ""
    for nome, chave, ids, desc in OBJ_FONO:
        links = "".join(f'<li><a href="{P[i]["slug"]}.html"><img src="img/loja/card_{i}.jpg" alt="" loading="lazy" width="80" height="100"><span><b>{e(P[i]["nome"])}</b><small>{reais(P[i]["preco"])} · {P[i]["paginas"]} páginas</small></span></a></li>' for i in ids)
        objetivos += f'<div class="fh-obj surge"><h3>{e(nome)}</h3><p>{e(desc)}</p><ul>{links}</ul></div>'
    por_dentro = [("img/kits/t01_pg26.jpg", "Fala em Foco: pares mínimos"), ("img/kits/t01_pg31.jpg", "Fala em Foco: escada da fala"),
                  ("img/kits/t02_pg05.jpg", "Motricidade Orofacial"), ("img/kits/t08_pg04.jpg", "Cartas de Linguagem: vocabulário"),
                  ("img/kits/t08_pg23.jpg", "Cartas de Linguagem: adivinhas"), ("img/kits/t06_pg04.jpg", "Consultório em Ordem: anamnese infantil"),
                  ("img/kits/t06_pg12.jpg", "Consultório em Ordem: plano terapêutico"), ("img/kits/t07_pg18.jpg", "Palavra Viva: objetos da casa")]
    vids = "".join(f'<figure class="video pagina surge"><video data-auto muted loop playsinline preload="none" poster="video/{a}.jpg"><source src="video/{a}.mp4" type="video/mp4"></video><button class="play" type="button" data-play></button><figcaption><b>{e(t)}</b><span>Vídeo demonstrativo · páginas reais</span></figcaption></figure>'
                   for a, t in [("t01", "Fala em Foco por dentro"), ("fono3", "Combo Fono por dentro"), ("t02", "Motricidade Orofacial por dentro")])
    outros = [("para-familias.html", "Famílias", "Cadernos e jogos educativos para fazer em casa. Atividades lúdicas, sem instrumentos de avaliação."),
              ("para-professoras.html", "Professoras e educadoras", "Consciência fonológica, alfabetização, atenção e rotina para a sala de aula."),
              ("para-terapeutas.html", "Psicopedagogas e terapeutas", "Comunicação alternativa, emoções, rotina e funções de atenção."),
              ("para-escolas.html", "Escolas e instituições", "Materiais por objetivo para a equipe, com licença individual por profissional.")]
    outros_html = "".join(f'<a class="fh-outro" href="{a}"><b>{e(t)}</b><span>{e(d)}</span><i>{ic("seta", "")}</i></a>' for a, t, d in outros)
    faq = [("Qual é o formato dos materiais?", "Arquivos em PDF, tamanho A4, para imprimir. O Consultório em Ordem também vem em Word para editar com o seu logotipo. Nada é enviado pelo correio."),
           ("Preciso de impressora colorida?", "Não é obrigatório. Os cartões e pranchas ficam mais fáceis de reconhecer em cores, e as fichas funcionam bem em preto e branco. Papel 180 g ou plastificação aumentam a durabilidade dos cartões."),
           ("Como recebo o acesso?", "Depois da confirmação do pagamento, a Eduzz envia o link do material para o e-mail informado na compra. Cartão e Pix costumam ser confirmados em minutos; boleto pode levar até 3 dias úteis."),
           ("Posso usar com todos os meus pacientes?", "Sim. A licença permite imprimir quantas vezes precisar para usar com os seus pacientes e mandar atividades para casa. Cada profissional que usa o arquivo precisa da própria compra; não é permitido repassar o PDF."),
           ("Como funciona a compra?", "Pagamento único, sem mensalidade, na página segura da Eduzz. As formas de pagamento aparecem na própria Eduzz no momento da compra."),
           ("E se eu não gostar?", "Você tem 7 dias depois do pagamento para pedir o dinheiro de volta pela área de compras da Eduzz ou pelo nosso atendimento, sem precisar explicar o motivo (Código de Defesa do Consumidor, art. 49)."),
           ("Os materiais substituem avaliação ou protocolo?", "Não. São recursos complementares. Não fazem diagnóstico, não são instrumentos padronizados e dependem da seleção e da adaptação da fonoaudióloga responsável."),
           ("Como falo com o suporte?", f"Pelo WhatsApp {WHATS_TXT}, em horário comercial, ou pelo e-mail que aparece no rodapé desta página.")]
    faq_html = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    corpo = f'''
<section class="hero-split fh-hero">
  <div class="envoltorio">
    <div class="texto">
      <p class="sobretitulo">Para fonoaudiólogas que atendem crianças</p>
      <h1>Menos tempo preparando materiais. Mais tempo para seus atendimentos.</h1>
      <p class="intro">Recursos imprimíveis de fala e linguagem para fonoaudiólogas que atendem crianças. Escolha, imprima e adapte às necessidades de cada atendimento.</p>
      <div class="botoes">
        <a class="btn btn-acao" href="{KIT_URL}?origem=home_hero" data-kit-gratis>Conhecer o Kit Grátis da Fono {ic("seta", "")}</a>
        <a class="btn btn-linha" href="categoria-fonoaudiologia-e-terapias.html">Explorar materiais completos</a>
      </div>
      <ul class="hero-fatos"><li><b>{fono}</b> materiais de fonoaudiologia</li><li><b>{n}</b> materiais na loja</li><li><b>7 dias</b> para desistir da compra</li></ul>
    </div>
    <div class="fh-pilha" aria-label="Páginas reais dos materiais">
      <figure class="p1"><img src="img/kits/t01_pg26.jpg" alt="Página real do Fala em Foco: pares mínimos" fetchpriority="high"></figure>
      <figure class="p2"><img src="img/kits/t08_pg04.jpg" alt="Página real das Cartas de Linguagem: cartas de vocabulário"></figure>
      <figure class="p3"><img src="img/kits/t06_pg04.jpg" alt="Página real do Consultório em Ordem: anamnese infantil"></figure>
      <span class="fh-rotulo">Páginas reais dos kits</span>
    </div>
  </div>
</section>
<section class="garantias" aria-label="Como funciona">
  <div class="envoltorio"><ul>
    <li>{ic("pdf")}<div><b>PDF para imprimir</b>enviado por e-mail pela Eduzz</div></li>
    <li>{ic("impressora")}<div><b>Imprima à vontade</b>para os seus pacientes</div></li>
    <li>{ic("cadeado")}<div><b>Pagamento único</b>processado pela Eduzz</div></li>
    <li>{ic("escudo")}<div><b>7 dias</b>para pedir o dinheiro de volta</div></li>
  </ul></div>
</section>

<section class="secao" id="kit-gratis">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Kit Grátis da Fono</p><h2>Conheça os materiais antes de comprar</h2><p class="intro">Uma amostra de 15 páginas com quatro recursos prontos, para usar na sua próxima sessão.</p></div></div>
    {bloco_kit("origem=home_kit")}
  </div>
</section>

<section class="secao creme" id="combo">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Oferta principal</p><h2>Combo Fono: três kits para o consultório</h2><p class="intro">Documentos clínicos, atividades para adultos e idosos e cartas de linguagem para crianças, no mesmo padrão visual.</p></div></div>
    <article class="oferta grande fh-combo surge">
      <div class="img"><img src="img/loja/card_fono3.jpg" alt="Capas dos kits Consultório em Ordem, Palavra Viva e Cartas de Linguagem" loading="lazy"></div>
      <div class="txt">
        <span class="etq combo">3 kits · {combo["paginas"]} páginas + 22 arquivos Word</span>
        <h3>{e(combo["nome"])}</h3>
        <ul class="fh-inclui">{combo_itens}</ul>
        <p><b>Formato e acesso:</b> {e(combo["formato_longo"])}. {e(combo["entrega"])}, depois da confirmação do pagamento.</p>
        <div class="valores"><span class="preco">{reais(combo["preco"])}</span><span class="economia">Os três kits avulsos somam {reais(combo["de"])}</span></div>
        <div class="btns"><a class="btn btn-acao" href="combo-fono.html">Ver o Combo Fono por dentro {ic("seta", "")}</a><a class="btn btn-linha" href="#" data-checkout="fono3" data-sem-view data-comprar="Comprar por {reais(combo["preco"])}">Comprar</a></div>
      </div>
    </article>
  </div>
</section>

<section class="secao" id="objetivos">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Encontre por objetivo</p><h2>O que você quer trabalhar?</h2><p class="intro">Só aparecem aqui materiais que existem na loja. Toque para ver as páginas por dentro.</p></div><a class="link-seta" href="categoria-fonoaudiologia-e-terapias.html">Todos de fonoaudiologia {ic("seta", "")}</a></div>
    <div class="fh-objs">{objetivos}</div>
  </div>
</section>

<section class="secao creme" id="por-dentro">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Conheça os materiais por dentro</p><h2>Páginas reais, do jeito que saem na impressora</h2><p class="intro">Toque numa página para ampliar.</p></div>{setas()}</div>
    {galeria(por_dentro, "Por dentro")}
    <div class="videos fh-videos">{vids}</div>
  </div>
</section>

<section class="secao" id="quem-faz">
  <div class="envoltorio dupla">
    <div class="surge">
      <p class="sobretitulo">Quem faz</p>
      <h2>Uma editora pequena de materiais de apoio</h2>
      <p>O Acervo Essencial é uma marca de Ramon Werneck Julio, de Goiânia (GO). Os materiais são escritos, ilustrados e diagramados pela equipe editorial do Acervo, com ilustrações próprias num estilo único e páginas testadas na impressão.</p>
      <p>As orientações de cada kit seguem a literatura publicada citada nos próprios materiais. Os kits ainda não passaram por revisão técnica formal de uma fonoaudióloga; quando houver revisão, o nome e o registro da revisora aparecerão aqui e nos materiais revisados.</p>
      <p>Dúvidas, correções e sugestões de profissionais são bem-vindas pelo WhatsApp {WHATS_TXT}.</p>
      <a class="btn btn-linha" href="sobre.html" style="margin-top:12px">Sobre o Acervo e identificação do vendedor {ic("seta", "")}</a>
    </div>
    <div class="fh-mesa surge"><img src="img/kits/t01_mesa.jpg" alt="Páginas impressas do Fala em Foco sobre a mesa" loading="lazy"></div>
  </div>
</section>

<section class="secao creme" id="outros-publicos">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Outros públicos</p><h2>Não é fonoaudióloga?</h2><p class="intro">O Acervo também tem materiais educativos para casa e para a escola. Recursos de uso profissional ficam identificados em cada página.</p></div><a class="link-seta" href="loja.html">Ver a loja completa {ic("seta", "")}</a></div>
    <div class="fh-outros">{outros_html}</div>
    <p class="fh-amostra" id="amostra">Para famílias e professoras: <a href="amostra_gratis_P01.pdf" target="_blank" rel="noopener">baixe a amostra grátis do caderno Brincando com os Sons</a> (16 páginas, sem cadastro).</p>
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
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Acervo Essencial", "url": BASE, "logo": BASE + "apple-touch-icon.png", "sameAs": [FACEBOOK]}
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    return (g.cabeca("Acervo Essencial · materiais de fala e linguagem para fonoaudiólogas",
                     "Recursos imprimíveis de fala e linguagem para fonoaudiólogas que atendem crianças: pares mínimos, cartas de linguagem, motricidade orofacial e documentos clínicos. Kit grátis para conhecer.",
                     "index.html", "img/loja/og_kit.jpg", extra) + g.topo() + corpo + g.rodape(SCRIPT_KIT))

# Clique em botões que levam ao Kit Grátis: evento personalizado (não é Lead; Lead só depois do cadastro confirmado).
SCRIPT_KIT = '''<script>
document.querySelectorAll("[data-kit-gratis]").forEach(function (a) {
  a.addEventListener("click", function () { if (window.fbq) fbq("trackCustom", "CliqueKitGratis", { origem: location.pathname.split("/").pop() || "index.html" }); });
});
</script>
'''

def pagina_kit():
    paginas = galeria([(KG + a, b) for a, b in KIT_PAGINAS], "Kit Grátis da Fono")
    itens = "".join(f'<li><span class="fh-num">{i + 1}</span><div><b>{e(t)}</b><span>{e(d)}</span></div></li>' for i, (t, d) in enumerate(KIT_ITENS))
    faq = [("É realmente gratuito?", "Sim. O kit não custa nada e não gera cobrança. O cadastro serve para enviar o arquivo ao seu e-mail."),
           ("Qual é o formato?", "Um PDF de 15 páginas em A4, para imprimir em papel comum. Os cartões duram mais em papel 180 g ou plastificados."),
           ("Como recebo?", "Você toca no botão, preenche o cadastro na página da Eduzz, a plataforma que entrega os materiais do Acervo, e recebe o acesso ao PDF no e-mail informado."),
           ("Posso imprimir?", "Sim, quantas vezes precisar, para usar nos seus atendimentos e estudos."),
           ("Posso compartilhar o PDF?", "Por favor, não envie o arquivo. Para indicar a uma colega, compartilhe o endereço desta página: assim ela recebe a versão mais recente."),
           ("Substitui avaliação fonoaudiológica?", "Não. A ficha de observação é um roteiro de registro, não é teste padronizado nem instrumento de diagnóstico. Todo o material depende da seleção e da adaptação da fonoaudióloga responsável."),
           ("Vou receber propaganda?", "O cadastro é usado para entregar o kit. Novidades e ofertas só serão enviadas se você concordar separadamente, e você pode pedir para sair a qualquer momento.")]
    faq_html = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    btn = lambda txt, origem: f'<a class="btn btn-acao fh-cta" href="#" data-checkout="kitgratis" data-kit-gratis data-origem="{origem}" data-avise="{txt}" data-mensagem="Olá! Quero receber o Kit Grátis da Fono.">{txt} {ic("seta", "")}</a>'
    corpo = f'''
<section class="hero-split fh-hero">
  <div class="envoltorio">
    <div class="texto">
      <p class="sobretitulo">Acervo Essencial</p>
      <h1>Conheça gratuitamente os materiais que podem facilitar sua rotina de atendimento infantil.</h1>
      <p class="intro">Receba uma amostra de recursos imprimíveis de fala, linguagem e organização profissional para conhecer a qualidade do Acervo Essencial.</p>
      <div class="botoes">{btn("Receber meu kit gratuito", "hero")}</div>
      <ul class="hero-fatos"><li><b>15</b> páginas em PDF</li><li><b>4</b> recursos prontos</li><li><b>R$ 0</b> sem cobrança</li></ul>
    </div>
    <div class="fh-pilha">
      <figure class="p1"><img src="{KG}kg-01.jpg" alt="Capa do Kit Grátis da Fono" fetchpriority="high"></figure>
      <figure class="p2"><img src="{KG}kg-05.jpg" alt="Página de pares mínimos do kit"></figure>
      <figure class="p3"><img src="{KG}kg-10.jpg" alt="Página de cartas de linguagem do kit"></figure>
      <span class="fh-rotulo">Páginas reais do kit</span>
    </div>
  </div>
</section>

<section class="secao" id="inclui">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">O que está incluso</p><h2>Quatro recursos, 15 páginas</h2></div></div>
    <ul class="fh-lista fh-lista-2">{itens}</ul>
  </div>
</section>

<section class="secao creme" id="demonstracao">
  <div class="envoltorio">
    <div class="cabeca-secao surge"><div><p class="sobretitulo">Demonstração</p><h2>Veja as páginas antes de receber</h2><p class="intro">Toque numa página para ampliar.</p></div>{setas()}</div>
    {paginas}
  </div>
</section>

<section class="secao" id="para-quem">
  <div class="envoltorio dupla">
    <div class="surge">
      <p class="sobretitulo">Para quem é</p>
      <h2>Para fonoaudiólogas que atendem crianças</h2>
      <p>O kit foi pensado como recurso complementar para a fonoaudiologia infantil: cartões e cartas para a sessão, fichas para o seu registro e uma anamnese que completa a que você já usa.</p>
      <p>Cada página depende da sua seleção e adaptação para os objetivos de cada criança. Estudantes de Fonoaudiologia podem usar em estágio, sob supervisão de profissional habilitado.</p>
      <p>As fichas não são para uso autônomo de familiares.</p>
    </div>
    <div class="surge">
      <p class="sobretitulo">Como receber</p>
      <ol class="fh-passos">
        <li><b>Toque no botão</b><span>Você vai para a página segura da Eduzz, que entrega os materiais do Acervo.</span></li>
        <li><b>Faça o cadastro</b><span>Nome e e-mail para a entrega. Não pedimos dados de pacientes.</span></li>
        <li><b>Receba o acesso ao PDF</b><span>O link de acesso chega no e-mail informado no cadastro. Confira também o spam e a aba Promoções.</span></li>
      </ol>
      {btn("Receber meu kit gratuito", "como_receber")}
    </div>
  </div>
</section>

<section class="secao creme" id="identificacao">
  <div class="envoltorio texto-longo">
    <p class="sobretitulo">Quem faz</p>
    <h2>Acervo Essencial</h2>
    <p>Marca de Ramon Werneck Julio, de Goiânia (GO). O kit foi escrito, ilustrado e diagramado pela equipe editorial do Acervo a partir de páginas dos kits Fala em Foco, Cartas de Linguagem e Consultório em Ordem.</p>
    <p><b>Revisão técnica:</b> este kit ainda não passou por revisão formal de uma fonoaudióloga. Quando houver, o nome e o registro da revisora serão informados aqui.</p>
  </div>
</section>

<section class="secao" id="perguntas">
  <div class="envoltorio">
    <div class="cabeca-secao surge" style="justify-content:center;text-align:center"><div><p class="sobretitulo">Perguntas frequentes</p><h2>Sobre o Kit Grátis</h2></div></div>
    <div class="faq">{faq_html}</div>
  </div>
</section>

<section class="secao escura" id="receber">
  <div class="envoltorio" style="text-align:center">
    <h2>Quer ver o padrão dos materiais na sua próxima sessão?</h2>
    <p class="intro" style="margin:0 auto 28px;color:#C9D8DC">15 páginas para imprimir, sem custo.</p>
    {btn("Quero conhecer os materiais gratuitamente", "cta_final")}
  </div>
</section>
'''
    return (g.cabeca("Kit Grátis da Fono · Acervo Essencial",
                     "Amostra gratuita para fonoaudiólogas que atendem crianças: ficha de observação dos sons, 20 cartões de pares mínimos, 10 cartas de linguagem e anamnese complementar. PDF de 15 páginas.",
                     KIT_URL, KG + "kg-01.jpg") + g.topo() + corpo + g.rodape(SCRIPT_KIT))

def pagina_obrigado():
    combo = P["fono3"]
    corpo = f'''
<section class="secao" style="padding-top:56px">
  <div class="envoltorio texto-longo">
    <p class="sobretitulo">Cadastro confirmado</p>
    <h1 style="font-size:clamp(32px,4vw,46px)">Seu Kit Grátis da Fono está a caminho</h1>
    <p class="intro">O link de acesso ao PDF vai para o e-mail que você informou no cadastro. Se não aparecer em alguns minutos, confira o spam e a aba Promoções.</p>
    <p>Problemas para receber? Fale pelo WhatsApp {WHATS_TXT}.</p>
  </div>
</section>
<section class="secao creme">
  <div class="envoltorio">
    <div class="cabeca-secao"><div><p class="sobretitulo">Para quando quiser mais</p><h2>{e(combo["nome"])}</h2><p class="intro">{e(combo["resumo"])}</p></div></div>
    <div class="btns" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-acao" href="combo-fono.html?utm_source=obrigado_kit">Ver o Combo Fono por dentro {ic("seta", "")}</a><a class="btn btn-linha" href="categoria-fonoaudiologia-e-terapias.html">Todos os materiais de fonoaudiologia</a></div>
  </div>
</section>
'''
    # Lead só dispara aqui, na página para onde a Eduzz redireciona depois do cadastro concluído.
    lead = '<script>if (window.fbq) fbq("track", "Lead", { content_name: "Kit Grátis da Fono", content_ids: ["kitgratis"], value: 0, currency: "BRL" });</script>\n'
    return (g.cabeca("Cadastro confirmado · Kit Grátis da Fono", "Confirmação do cadastro do Kit Grátis da Fono.", "obrigado-kit-gratis.html", KG + "kg-01.jpg",
                     '<meta name="robots" content="noindex">\n') + g.topo() + corpo + g.rodape(lead))
