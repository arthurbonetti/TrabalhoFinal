for $fornecedor in doc('fornecedor.xml')/dados/fornecedor
where $fornecedor/Cidade = 'LONDRES'
return (
  replace value of node $fornecedor/Status with 50
)
