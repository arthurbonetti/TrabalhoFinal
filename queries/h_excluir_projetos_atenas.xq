for $projeto in doc('../fornecedor/projeto.xml')/dados/projeto
where $projeto/Cidade = 'ATENAS'
return (
  delete node $projeto
)
