for $projeto in doc('projeto.xml')/dados/projeto
where $projeto/Cidade = 'PARIS'
return $projeto/Jnome
