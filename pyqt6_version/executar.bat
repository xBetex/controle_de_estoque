@echo off
echo ================================================
echo       Sistema de Controle de Estoque
echo ================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Por favor, instale o Python 3.8 ou superior.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Verificar se as dependências estão instaladas
echo Verificando dependências...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependências!
        pause
        exit /b 1
    )
) else (
    echo Dependências OK!
)

echo.
echo Iniciando sistema...
echo.

REM Executar o sistema
python main.py

REM Pausa se houver erro
if errorlevel 1 (
    echo.
    echo ERRO: Falha ao executar o sistema!
    echo Verifique o arquivo de log para mais detalhes.
    pause
) 