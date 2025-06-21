#!/bin/bash

echo "================================================"
echo "       Sistema de Controle de Estoque"
echo "================================================"
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERRO: Python não encontrado!"
        echo "Por favor, instale o Python 3.8 ou superior."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python encontrado!"
echo

# Verificar se as dependências estão instaladas
echo "Verificando dependências..."
$PYTHON_CMD -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao instalar dependências!"
        exit 1
    fi
else
    echo "Dependências OK!"
fi

echo
echo "Iniciando sistema..."
echo

# Executar o sistema
$PYTHON_CMD main.py

# Verificar se houve erro
if [ $? -ne 0 ]; then
    echo
    echo "ERRO: Falha ao executar o sistema!"
    echo "Verifique o arquivo de log para mais detalhes."
fi 