// Acervo Essencial · comportamento da loja: menu, busca, filtros, galerias, vídeos e barra de compra.
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var norm = function (t) { return (t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };

  // Submenus do topo (clique, teclado e clique fora)
  $$(".menu .sub > button").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      var sub = b.parentNode, aberto = sub.classList.contains("aberto");
      $$(".menu .sub").forEach(function (s) { s.classList.remove("aberto"); s.firstElementChild.setAttribute("aria-expanded", "false"); });
      if (!aberto) { sub.classList.add("aberto"); b.setAttribute("aria-expanded", "true"); }
    });
  });
  document.addEventListener("click", function () { $$(".menu .sub").forEach(function (s) { s.classList.remove("aberto"); }); });

  // Gaveta do celular
  var gaveta = $(".gaveta");
  function abreGaveta(sim) { if (!gaveta) return; gaveta.classList.toggle("aberta", sim); document.body.style.overflow = sim ? "hidden" : ""; }
  $$("[data-abre-menu]").forEach(function (b) { b.addEventListener("click", function () { abreGaveta(true); }); });
  $$("[data-fecha-menu]").forEach(function (b) { b.addEventListener("click", function () { abreGaveta(false); }); });

  // Busca em todo o catálogo
  var busca = $(".busca"), campo = busca && $("input", busca), lista = busca && $(".resultados", busca);
  function preco(p) { return p.preco === 0 ? "Grátis" : "R$ " + p.preco.toFixed(2).replace(".", ","); }
  function procura(q) {
    var termos = norm(q).split(/\s+/).filter(Boolean);
    return (window.CATALOGO || []).filter(function (p) {
      return termos.every(function (t) { return p.busca.indexOf(t) >= 0; });
    });
  }
  function mostraBusca(q) {
    if (!lista) return;
    if (!q.trim()) { lista.innerHTML = ""; return; }
    var r = procura(q);
    lista.innerHTML = r.length ? r.map(function (p) {
      return '<a class="res" href="' + p.url + '"><img src="' + p.img + '" alt="" loading="lazy"><div><b>' + p.nome + '</b><span>' + p.linha + (p.idade ? " · " + p.idade : "") + '</span></div><em>' + preco(p) + '</em></a>';
    }).join("") : '<p class="vazio">Nenhum material encontrado para "' + q.replace(/</g, "") + '". Tente "rotina", "fala", "alfabetização" ou veja <a href="loja.html">todos os materiais</a>.</p>';
  }
  function abreBusca(sim) {
    if (!busca) return;
    busca.classList.toggle("aberta", sim);
    document.body.style.overflow = sim ? "hidden" : "";
    if (sim) { abreGaveta(false); setTimeout(function () { campo.focus(); }, 30); }
  }
  $$("[data-abre-busca]").forEach(function (b) { b.addEventListener("click", function () { abreBusca(true); }); });
  if (busca) {
    campo.addEventListener("input", function () { mostraBusca(campo.value); });
    busca.addEventListener("click", function (e) { if (e.target === busca || e.target.closest("[data-fecha-busca]")) abreBusca(false); });
    $$(".sugestoes button", busca).forEach(function (b) { b.addEventListener("click", function () { campo.value = b.textContent; mostraBusca(campo.value); campo.focus(); }); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { abreBusca(false); abreGaveta(false); }
    if (e.key === "/" && busca && !/input|textarea|select/i.test((document.activeElement || {}).tagName || "")) { e.preventDefault(); abreBusca(true); }
  });

  // Abas de perfil na página inicial
  $$("[data-abas]").forEach(function (grupo) {
    var abas = $$(".aba", grupo);
    abas.forEach(function (a) {
      a.addEventListener("click", function () {
        abas.forEach(function (x) { x.setAttribute("aria-selected", x === a ? "true" : "false"); var p = document.getElementById(x.getAttribute("aria-controls")); if (p) p.hidden = x !== a; });
      });
    });
  });

  // Filtros (loja e páginas de categoria): cada card tem data-cat, data-obj, data-pub, data-idade, data-formato
  $$("[data-filtravel]").forEach(function (area) {
    var cards = $$(".card", area.querySelector("[data-cards]") || area);
    var form = area.querySelector(".filtros") || area;
    var texto = area.querySelector("[data-busca-local]");
    var ordem = area.querySelector("[data-ordem]");
    var contagem = area.querySelector(".contagem");
    var nada = area.querySelector(".nada");
    var ativos = area.querySelector(".ativos");
    var grade = area.querySelector("[data-cards]");
    function marcados(nome) { return $$('input[name="' + nome + '"]:checked', form).map(function (i) { return i.value; }); }
    function chips(nome) { return $$('[data-chip="' + nome + '"][aria-pressed="true"]', area).map(function (b) { return b.value; }).filter(Boolean); }
    function bate(card, chave, vals) {
      if (!vals.length) return true;
      var tem = (card.getAttribute("data-" + chave) || "").split(" ");
      return vals.some(function (v) { return tem.indexOf(v) >= 0; });
    }
    function aplica() {
      var f = { cat: marcados("cat").concat(chips("cat")), obj: marcados("obj").concat(chips("obj")), pub: marcados("pub").concat(chips("pub")), idade: marcados("idade").concat(chips("idade")), formato: marcados("formato") };
      var q = norm(texto ? texto.value : "");
      var n = 0;
      cards.forEach(function (c) {
        var ok = bate(c, "cat", f.cat) && bate(c, "obj", f.obj) && bate(c, "pub", f.pub) && bate(c, "idade", f.idade) && bate(c, "formato", f.formato) &&
          (!q || q.split(/\s+/).every(function (t) { return (c.getAttribute("data-busca") || "").indexOf(t) >= 0; }));
        c.hidden = !ok; if (ok) n++;
      });
      if (contagem) contagem.textContent = n === 1 ? "1 material" : n + " materiais";
      if (nada) nada.hidden = n > 0;
      if (ativos) {
        var html = "";
        $$("input:checked", form).forEach(function (i) { html += '<button type="button" data-tira="' + i.name + ":" + i.value + '">' + i.parentNode.textContent.replace(/\d+$/, "").trim() + ' <svg viewBox="0 0 12 12"><path d="M2 2l8 8M10 2l-8 8" stroke="currentColor" stroke-width="1.8"/></svg></button>'; });
        ativos.innerHTML = html;
        $$("button", ativos).forEach(function (b) { b.onclick = function () { var p = b.getAttribute("data-tira").split(":"); var i = form.querySelector('input[name="' + p[0] + '"][value="' + p[1] + '"]'); if (i) { i.checked = false; aplica(); } }; });
      }
      if (ordem && grade) {
        var o = ordem.value, vis = cards.slice();
        vis.sort(function (a, b) {
          var pa = +a.getAttribute("data-preco"), pb = +b.getAttribute("data-preco");
          if (o === "menor") return pa - pb;
          if (o === "maior") return pb - pa;
          if (o === "az") return a.getAttribute("data-nome").localeCompare(b.getAttribute("data-nome"), "pt");
          return +a.getAttribute("data-ordem") - +b.getAttribute("data-ordem");
        });
        vis.forEach(function (c) { grade.appendChild(c); });
      }
    }
    $$("input[type=checkbox]", form).forEach(function (i) { i.addEventListener("change", aplica); });
    $$("[data-chip]", area).forEach(function (b) {
      b.addEventListener("click", function () {
        var grupoChip = $$('[data-chip="' + b.getAttribute("data-chip") + '"]', area);
        var ligado = b.getAttribute("aria-pressed") === "true";
        grupoChip.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        if (!ligado && b.value) b.setAttribute("aria-pressed", "true");
        if (!b.value) b.setAttribute("aria-pressed", "true");
        aplica();
      });
    });
    if (texto) texto.addEventListener("input", aplica);
    if (ordem) ordem.addEventListener("change", aplica);
    var limpa = area.querySelector("[data-limpa]");
    if (limpa) limpa.addEventListener("click", function () { $$("input:checked", form).forEach(function (i) { i.checked = false; }); if (texto) texto.value = ""; aplica(); });
    // Filtro pré-selecionado pelo endereço: loja.html#cat-autismo, #obj-fala, #pub-fono, #idade-3a5
    function doHash() {
      var h = (location.hash || "").slice(1), m = h.match(/^(cat|obj|pub|idade|formato)-(.+)$/);
      if (!m) return;
      $$("input:checked", form).forEach(function (i) { i.checked = false; });
      var i = form.querySelector('input[name="' + m[1] + '"][value="' + m[2] + '"]');
      if (i) i.checked = true;
      aplica();
    }
    window.addEventListener("hashchange", doHash);
    doHash();
    // Gaveta de filtros no celular
    $$("[data-abre-filtros]", area).forEach(function (b) { b.addEventListener("click", function () { form.classList.add("aberto"); }); });
    $$("[data-fecha-filtros]", area).forEach(function (b) { b.addEventListener("click", function () { form.classList.remove("aberto"); }); });
    aplica();
  });

  // Galeria do produto: miniaturas trocam a imagem principal
  $$(".vitrine").forEach(function (v) {
    var principal = $(".principal img", v), btnPrincipal = $(".principal", v);
    $$(".miniaturas button", v).forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".miniaturas button", v).forEach(function (x) { x.removeAttribute("aria-current"); });
        b.setAttribute("aria-current", "true");
        principal.src = b.getAttribute("data-img");
        principal.alt = b.getAttribute("data-legenda");
        btnPrincipal.setAttribute("data-zoom", b.getAttribute("data-img"));
        btnPrincipal.setAttribute("data-legenda", b.getAttribute("data-legenda"));
      });
    });
  });

  // Visualização ampliada de páginas (sem animação)
  var dlg = document.createElement("dialog");
  dlg.className = "zoom";
  dlg.innerHTML = '<button class="z-fechar" type="button">Fechar</button><button class="z-ant" type="button" aria-label="Anterior">&lsaquo;</button><figure><img alt=""><figcaption></figcaption></figure><button class="z-prox" type="button" aria-label="Próxima">&rsaquo;</button>';
  document.body.appendChild(dlg);
  var zImg = $("img", dlg), zCap = $("figcaption", dlg), zLista = [], zAt = 0;
  function zMostra(i) { zAt = (i + zLista.length) % zLista.length; var b = zLista[zAt]; zImg.src = b.getAttribute("data-zoom"); zCap.textContent = b.getAttribute("data-legenda") || ""; }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-zoom]");
    if (!b || dlg.contains(b)) return;
    var grupo = b.closest("[data-grupo]");
    zLista = grupo ? $$("[data-zoom]", grupo) : [b];
    zMostra(Math.max(0, zLista.indexOf(b)));
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
  });
  $(".z-fechar", dlg).onclick = function () { dlg.close(); };
  $(".z-ant", dlg).onclick = function () { zMostra(zAt - 1); };
  $(".z-prox", dlg).onclick = function () { zMostra(zAt + 1); };
  dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.tagName === "FIGURE") dlg.close(); });
  document.addEventListener("keydown", function (e) { if (!dlg.open) return; if (e.key === "ArrowLeft") zMostra(zAt - 1); if (e.key === "ArrowRight") zMostra(zAt + 1); });

  // Setas dos trilhos de páginas
  $$(".rolo").forEach(function (r) {
    var t = $(".trilho", r);
    $$("[data-rolar]", r).forEach(function (s) { s.addEventListener("click", function () { t.scrollBy({ left: +s.getAttribute("data-rolar") * t.clientWidth * 0.8, behavior: "smooth" }); }); });
  });

  // Vídeos: tocam sem som quando aparecem na tela; botão para pausar
  var poucoMovimento = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var vids = $$("video[data-auto]");
  if ("IntersectionObserver" in window && !poucoMovimento) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) { if (!v.dataset.pausado) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } }
        else v.pause();
      });
    }, { threshold: 0.4 });
    vids.forEach(function (v) { v.preload = "metadata"; io.observe(v); });
  }
  $$("[data-play]").forEach(function (b) {
    var v = b.parentNode.querySelector("video");
    function icone() { b.innerHTML = v.paused ? '<svg viewBox="0 0 20 20"><path d="M6 4l10 6-10 6z" fill="currentColor"/></svg>' : '<svg viewBox="0 0 20 20"><path d="M5 4h3v12H5zM12 4h3v12h-3z" fill="currentColor"/></svg>'; b.setAttribute("aria-label", v.paused ? "Tocar vídeo" : "Pausar vídeo"); }
    b.addEventListener("click", function () { if (v.paused) { delete v.dataset.pausado; v.play(); } else { v.dataset.pausado = "1"; v.pause(); } });
    v.addEventListener("play", icone); v.addEventListener("pause", icone); icone();
  });

  // Barra de compra fixa no celular (aparece depois que o botão principal sai da tela)
  var barra = $(".barra-compra"), alvo = $("[data-alvo-barra]");
  if (barra && alvo) {
    var pendente = false;
    var confere = function () { pendente = false; barra.classList.toggle("visivel", alvo.getBoundingClientRect().bottom < 0); };
    window.addEventListener("scroll", function () { if (!pendente) { pendente = true; requestAnimationFrame(confere); } }, { passive: true });
    confere();
  }

  // Entrada suave dos blocos
  var surgem = $$(".surge");
  if ("IntersectionObserver" in window && !poucoMovimento) {
    var io2 = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("visto"); io2.unobserve(en.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    surgem.forEach(function (s) { io2.observe(s); });
  } else surgem.forEach(function (s) { s.classList.add("visto"); });
})();
