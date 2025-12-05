for $projeto in doc('../fornecedor/projeto.xml')/dados/projeto
where $projeto/Cidade = 'PARIS'
return $projeto/Jnome
