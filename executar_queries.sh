#!/bin/bash

# Script para executar todas as queries XQuery e organizar resultados
# Criado em: 2025-12-05

# Cores para output
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretórios (relativos ao local do script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUERIES_DIR="$SCRIPT_DIR/queries"
FORNECEDOR_DIR="$SCRIPT_DIR/fornecedor"
RESULTADOS_DIR="$SCRIPT_DIR/resultados"

# Criar pasta de resultados se não existir
mkdir -p "$RESULTADOS_DIR"

# Limpar resultados anteriores
rm -f "$RESULTADOS_DIR"/*.txt

echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${BLUE}  EXECUTANDO TODAS AS QUERIES XQUERY${NC}"
echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════════${NC}\n"

# Função para executar query
executar_query() {
    local letra=$1
    local descricao=$2
    local arquivo=$3
    
    echo -e "${BOLD}${GREEN}[$letra]${NC} $descricao"
    echo "════════════════════════════════════════════════════════" >> "$RESULTADOS_DIR/RESULTADOS_COMPLETOS.txt"
    echo "$letra) $descricao" >> "$RESULTADOS_DIR/RESULTADOS_COMPLETOS.txt"
    echo "════════════════════════════════════════════════════════" >> "$RESULTADOS_DIR/RESULTADOS_COMPLETOS.txt"
    
    # Executar a query e capturar resultado
    resultado=$(cd "$FORNECEDOR_DIR" && basex "$QUERIES_DIR/$arquivo" 2>&1)
    
    # Salvar resultado em arquivo individual
    echo "$resultado" > "$RESULTADOS_DIR/${letra}_${arquivo%.xq}.txt"
    
    # Adicionar ao arquivo completo
    echo "$resultado" >> "$RESULTADOS_DIR/RESULTADOS_COMPLETOS.txt"
    echo "" >> "$RESULTADOS_DIR/RESULTADOS_COMPLETOS.txt"
    
    echo -e "${GREEN}✓ Concluído${NC}\n"
}

# Executar cada query
executar_query "a" "Retornar os dados da penúltima peça da árvore XML" "a_penultima_peca.xq"
executar_query "b" "Inserir um atributo com a data em todos os fornecimentos" "b_inserir_data_fornecimentos.xq"
executar_query "c" "Atualizar o status dos fornecedores de Londres para 50" "c_atualizar_status_londres.xq"
executar_query "d" "Retornar o código, a cidade e cor de todas as peças" "d_codigo_cidade_cor.xq"
executar_query "e" "Obter o somatório das quantidades dos fornecimentos" "e_somatrio_quantidades.xq"
executar_query "f" "Obter os nomes dos projetos de Paris" "f_projetos_paris.xq"
executar_query "g" "Obter o código dos fornecedores que forneceram peças em maior quantidade" "g_fornecedor_maior_quantidade.xq"
executar_query "h" "Excluir os projetos da cidade de Atenas" "h_excluir_projetos_atenas.xq"
executar_query "i" "Obter os nomes das peças e seus dados de fornecimento" "i_pecas_fornecimentos.xq"
executar_query "j" "Obter o preço médio das peças" "j_preco_medio.xq"

echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${GREEN}✓ TODAS AS QUERIES FORAM EXECUTADAS COM SUCESSO!${NC}"
echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}Arquivos de resultado criados em:${NC}"
echo -e "${GREEN}$RESULTADOS_DIR${NC}\n"

echo -e "${YELLOW}Arquivos gerados:${NC}"
ls -lh "$RESULTADOS_DIR" | tail -n +2 | awk '{print "  " $9 " (" $5 ")"}'

echo -e "\n${YELLOW}Para visualizar todos os resultados:${NC}"
echo -e "${GREEN}cat $RESULTADOS_DIR/RESULTADOS_COMPLETOS.txt${NC}\n"
