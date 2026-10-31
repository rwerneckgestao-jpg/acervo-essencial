// Links de compra da Eduzz. Preencha cada um quando o produto estiver ativo; vazio = botão leva à amostra grátis
// (cadernos) ou ao "Avise-me" pelo WhatsApp (kits terapêuticos).
var CHECKOUT = {
  kit: "https://chk.eduzz.com/Q9N28ZPK01",
  p01: "https://chk.eduzz.com/40QR7Z1Q9B",
  p02: "https://chk.eduzz.com/Z0B1RNEJ9A",
  p03: "https://chk.eduzz.com/E9OGXJ8GWB",
  p04: "https://chk.eduzz.com/R9JXOZ7P0X",
  t01: "",
  t02: "",
  t03: "",
  t04: "",
  colecao: ""
};
// Nome e preço de cada produto, para os eventos do Pixel e a mensagem do WhatsApp.
var PRODUTO = {
  kit: ["Kit Completo", 39.90],
  p01: ["Brincando com os Sons", 19.90],
  p02: ["Letras que Viram Palavras", 19.90],
  p03: ["Cobra e Abelha", 19.90],
  p04: ["Olhos Atentos", 19.90],
  t01: ["Fala em Foco", 19.90],
  t02: ["Motricidade Orofacial", 19.90],
  t03: ["Comunica", 19.90],
  t04: ["Emoções e Regulação", 19.90],
  colecao: ["Coleção com os 4 kits", 47]
};
var WHATSAPP = "5562993375885";
// Parâmetros de rastreamento: guardados na primeira visita e repassados ao checkout.
var RASTREIO = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "src", "sck", "fbclid"];
function rastreio() {
  var guardado = {}, url = new URLSearchParams(location.search);
  try { guardado = JSON.parse(sessionStorage.getItem("ae_utm") || "{}"); } catch (e) {}
  RASTREIO.forEach(function (k) { if (url.get(k)) guardado[k] = url.get(k); });
  try { sessionStorage.setItem("ae_utm", JSON.stringify(guardado)); } catch (e) {}
  return guardado;
}
var UTM = rastreio();
function comUtm(link) {
  var u = new URL(link);
  Object.keys(UTM).forEach(function (k) { if (!u.searchParams.has(k)) u.searchParams.set(k, UTM[k]); });
  return u.toString();
}
function evento(nome, chave) {
  if (!window.fbq) return;
  var p = PRODUTO[chave];
  fbq("track", nome, p ? { content_name: p[0], content_ids: [chave], content_type: "product", value: p[1], currency: "BRL" } : {});
}
document.querySelectorAll("[data-checkout]").forEach(function (a) {
  var chave = a.getAttribute("data-checkout");
  var url = CHECKOUT[chave];
  if (url) {
    a.href = comUtm(url); a.rel = "noopener";
    if (a.getAttribute("data-comprar")) a.textContent = a.getAttribute("data-comprar");
    a.addEventListener("click", function () { evento("InitiateCheckout", chave); });
  }
  else if (a.hasAttribute("data-avise")) {
    a.href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(a.getAttribute("data-mensagem") || "Olá! Quero saber do lançamento do kit " + PRODUTO[chave][0]);
    a.target = "_blank"; a.rel = "noopener";
    a.textContent = a.getAttribute("data-avise") || "Avise-me no lançamento";
    a.addEventListener("click", function () { evento("Contact", chave); });
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
