// Galerias de páginas: setas para rolar e visualização ampliada (sem animação).
(function () {
  var dlg = document.createElement("dialog");
  dlg.className = "zoom";
  dlg.innerHTML = '<button class="z-fechar" aria-label="Fechar">Fechar</button>' +
    '<button class="z-ant" aria-label="Página anterior">&lsaquo;</button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="z-prox" aria-label="Próxima página">&rsaquo;</button>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector("img"), cap = dlg.querySelector("figcaption");
  var lista = [], atual = 0;
  function mostra(i) {
    atual = (i + lista.length) % lista.length;
    var b = lista[atual];
    img.src = b.getAttribute("data-zoom");
    img.alt = b.querySelector("img").alt;
    cap.textContent = b.getAttribute("data-legenda") || img.alt;
  }
  document.querySelectorAll("[data-zoom]").forEach(function (b) {
    b.addEventListener("click", function () {
      var grupo = b.closest("[data-grupo]");
      lista = [].slice.call((grupo || document).querySelectorAll("[data-zoom]"));
      mostra(lista.indexOf(b));
      dlg.showModal();
    });
  });
  dlg.querySelector(".z-fechar").onclick = function () { dlg.close(); };
  dlg.querySelector(".z-ant").onclick = function () { mostra(atual - 1); };
  dlg.querySelector(".z-prox").onclick = function () { mostra(atual + 1); };
  dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
  document.addEventListener("keydown", function (e) {
    if (!dlg.open) return;
    if (e.key === "ArrowLeft") mostra(atual - 1);
    if (e.key === "ArrowRight") mostra(atual + 1);
  });
  document.querySelectorAll(".rolo").forEach(function (r) {
    var g = r.querySelector(".galeria");
    r.querySelectorAll("[data-rolar]").forEach(function (s) {
      s.onclick = function () { g.scrollBy({ left: +s.getAttribute("data-rolar") * g.clientWidth * 0.8 }); };
    });
  });
})();
