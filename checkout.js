// Links de compra da Eduzz. Preencha cada um quando o produto estiver ativo; vazio = botão leva à amostra grátis.
var CHECKOUT = {
  kit: "https://chk.eduzz.com/Q9N28ZPK01",
  p01: "https://chk.eduzz.com/40QR7Z1Q9B",
  p02: "https://chk.eduzz.com/Z0B1RNEJ9A",
  p03: "https://chk.eduzz.com/E9OGXJ8GWB",
  p04: "https://chk.eduzz.com/R9JXOZ7P0X"
};
// Nome e preço de cada produto, para os eventos do Pixel.
var PRODUTO = {
  kit: ["Kit Completo", 39.90],
  p01: ["Brincando com os Sons", 19.90],
  p02: ["Letras que Viram Palavras", 19.90],
  p03: ["Cobra e Abelha", 19.90],
  p04: ["Olhos Atentos", 19.90]
};
function evento(nome, chave) {
  if (!window.fbq) return;
  var p = PRODUTO[chave];
  fbq("track", nome, p ? { content_name: p[0], content_ids: [chave], content_type: "product", value: p[1], currency: "BRL" } : {});
}
document.querySelectorAll("[data-checkout]").forEach(function (a) {
  var chave = a.getAttribute("data-checkout");
  var url = CHECKOUT[chave];
  if (url) {
    a.href = url; a.rel = "noopener";
    a.addEventListener("click", function () { evento("InitiateCheckout", chave); });
  }
  else {
    a.href = a.closest("body").querySelector("#amostra") ? "#amostra" : "index.html#amostra";
    a.textContent = "Vendas abrem em breve · baixe a amostra grátis";
  }
});
// Página de produto: ViewContent do caderno (ou do kit, na página principal).
var principal = document.querySelector("[data-checkout]");
if (principal) evento("ViewContent", principal.getAttribute("data-checkout"));
// Download da amostra grátis conta como Lead.
document.querySelectorAll('a[href$=".pdf"]').forEach(function (a) {
  a.addEventListener("click", function () { if (window.fbq) fbq("track", "Lead", { content_name: "Amostra grátis" }); });
});
