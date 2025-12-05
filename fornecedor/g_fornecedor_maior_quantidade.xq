let $fornecimentos := doc('fornecimento.xml')/dados/fornecimento
let $maiorQtd := max($fornecimentos/Quantidade)
for $fornecimento in $fornecimentos
where $fornecimento/Quantidade = $maiorQtd
return distinct-values($fornecimento/Cod_Fornec)
