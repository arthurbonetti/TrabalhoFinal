let $hoje := current-date()
for $fornecimento in doc('fornecimento.xml')/dados/fornecimento
return (
  insert node attribute data { $hoje } into $fornecimento
)
