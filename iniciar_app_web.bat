@echo off
chcp 65001 >nul
title Extrator de Transcricao do YouTube - Web
cd /d "%~dp0"

echo ==========================================
echo   Extrator de Transcricao do YouTube (Web)
echo ==========================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado no seu computador.
    echo Baixe e instale em: https://www.python.org/downloads/
    echo IMPORTANTE: marque a opcao "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

python -c "import flask, youtube_transcript_api" >nul 2>nul
if %errorlevel% neq 0 (
    echo Instalando dependencias necessarias...
    python -m pip install -r requirements.txt --quiet
    if %errorlevel% neq 0 (
        echo.
        echo [ERRO] Falha ao instalar as dependencias. Verifique sua conexao com a internet.
        pause
        exit /b 1
    )
    echo Instalacao concluida.
    echo.
)

echo Abrindo o servidor local...
echo Acesse no navegador: http://localhost:5000
echo (Deixe esta janela aberta enquanto usa o app. Feche para encerrar.)
echo.

start "" http://localhost:5000
python app_web.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] O aplicativo fechou com um erro. Veja a mensagem acima.
    pause
)
