for $projeto in doc('projeto.xml')/dados/projeto
where $projeto/Cidade = 'ATENAS'
return (
  delete node $projeto
)
