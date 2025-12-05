let $hoje := current-date()
for $fornecimento in doc('../fornecedor/fornecimento.xml')/dados/fornecimento
return (
  insert node attribute data { $hoje } into $fornecimento
)
