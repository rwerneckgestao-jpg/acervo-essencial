// Links de compra da Eduzz. Preencha cada um quando o produto estiver ativo; vazio = botão leva à amostra grátis.
var CHECKOUT = {
  kit: "https://chk.eduzz.com/Q9N28ZPK01",
  p01: "https://chk.eduzz.com/40QR7Z1Q9B",
  p02: "https://chk.eduzz.com/Z0B1RNEJ9A",
  p03: "https://chk.eduzz.com/E9OGXJ8GWB",
  p04: "https://chk.eduzz.com/R9JXOZ7P0X"
};
document.querySelectorAll("[data-checkout]").forEach(function (a) {
  var url = CHECKOUT[a.getAttribute("data-checkout")];
  if (url) { a.href = url; a.rel = "noopener"; }
  else {
    a.href = a.closest("body").querySelector("#amostra") ? "#amostra" : "index.html#amostra";
    a.textContent = "Vendas abrem em breve · baixe a amostra grátis";
  }
});
