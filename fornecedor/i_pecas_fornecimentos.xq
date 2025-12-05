let $fornecimentos := doc('fornecimento.xml')/dados/fornecimento
let $pecas := doc('peca.xml')/dados/peca
for $peca in $pecas
return (
  <peca_fornecimento>
    <PNome>{ $peca/PNome/text() }</PNome>
    <Cod_Peca>{ $peca/Cod_Peca/text() }</Cod_Peca>
    <fornecimentos>
    {
      for $forn in $fornecimentos
      where $forn/Cod_Peca = $peca/Cod_Peca
      return (
        <fornecimento>
          <Cod_Fornec>{ $forn/Cod_Fornec/text() }</Cod_Fornec>
          <Cod_Proj>{ $forn/Cod_Proj/text() }</Cod_Proj>
          <Quantidade>{ $forn/Quantidade/text() }</Quantidade>
        </fornecimento>
      )
    }
    </fornecimentos>
  </peca_fornecimento>
)
