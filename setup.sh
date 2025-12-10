#!/bin/bash

echo "=================================="
echo "Sistema de Recomendação"
echo "=================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado."
    exit 1
fi

echo "✓ Python encontrado"
echo ""

# Ambiente virtual
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -q -r requirements.txt

echo ""
echo "✓ Pronto!"
echo ""
echo "Para executar: python app.py"
echo ""

