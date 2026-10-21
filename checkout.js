// Links de compra da Eduzz. Preencha cada um quando o produto estiver ativo; vazio = botão leva à amostra grátis.
var CHECKOUT = {
  kit: "",
  p01: "",
  p02: "",
  p03: "",
  p04: ""
};
document.querySelectorAll("[data-checkout]").forEach(function (a) {
  var url = CHECKOUT[a.getAttribute("data-checkout")];
  if (url) { a.href = url; a.rel = "noopener"; }
  else {
    a.href = a.closest("body").querySelector("#amostra") ? "#amostra" : "index.html#amostra";
    a.textContent = "Vendas abrem em breve · baixe a amostra grátis";
  }
});
