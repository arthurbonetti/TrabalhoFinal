for $peca in doc('peca.xml')/dados/peca
return (
  <peca_info>
    <Cod_Peca>{ $peca/Cod_Peca/text() }</Cod_Peca>
    <Cidade>{ $peca/Cidade/text() }</Cidade>
    <Cor>{ $peca/Cor/text() }</Cor>
  </peca_info>
)
