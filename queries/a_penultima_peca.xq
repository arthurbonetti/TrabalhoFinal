let $pecas := doc('../fornecedor/peca.xml')/dados/peca
let $total := count($pecas)
let $penultima := $total - 1
return $pecas[$penultima]
