# Acervo Essencial

Site de vendas dos cadernos para imprimir (GitHub Pages).

- `index.html`: página principal e Kit Completo.
- Uma página por caderno: `brincando-com-os-sons.html`, `letras-que-viram-palavras.html`, `cobra-e-abelha.html`, `olhos-atentos.html`.
- `checkout.js`: links de compra da Eduzz (cadernos p01–p04 e kit; kits terapêuticos t01–t04 e colecao). Enquanto um link está vazio, o botão dos cadernos leva à amostra grátis e o dos kits terapêuticos vira "Avise-me" no WhatsApp. Repassa utm_*, src, sck e fbclid ao checkout e dispara InitiateCheckout no clique.
- `pixel.js`: Pixel da Meta (1134422302272045). Eventos: PageView, ViewContent, InitiateCheckout (clique em comprar) e Lead (download da amostra), disparados em `checkout.js`.
- `politica-de-privacidade.html` e `termos-de-uso.html`: páginas legais, linkadas no rodapé de todas as páginas.
- `favicon.svg`, `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`: ícones do site.

## Padrão visual (16 regras, desde a v05)
Sem gradiente roxo, sem botões pílula, sem avaliações, métricas ou contadores falsos, título do topo concreto (diz o que é o produto),
sem ícones de emoji (ícones em SVG), sem travessões, sem animação exagerada ou de cursor, sem fotos geradas por IA (usar páginas reais
dos cadernos ou fotos reais), sem selo "feito com IA", favicon, política de privacidade e termos no rodapé. Domínio próprio: pendente.

## v06 (25/10/2026): o produto por dentro
- `img/`: páginas reais renderizadas dos PDFs finais (`img/pg/pC-NN.jpg`), mesa de páginas do topo (`hero_paginas.jpg`, `mesa_pC.jpg`), pilhas do kit, detalhes ampliados e a parede com todas as páginas de cada caderno (`todas_pC.jpg`).
- `galeria.css` e `galeria.js`: galerias com rolagem lateral e visualização ampliada (sem animação).

## Kits terapêuticos (28/10/2026)
- `kits-terapeuticos.html`: linha nova com visual editorial (Fraunces + Source Sans 3). Os 4 cadernos continuam em `index.html`, que ganhou uma faixa e um link no menu para a linha nova.
- `img/kits/`: montagens e páginas reais dos 4 kits, geradas dos PDFs finais.
