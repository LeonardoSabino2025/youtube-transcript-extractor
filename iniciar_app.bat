@echo off
chcp 65001 >nul
title Extrator de Transcricao do YouTube
cd /d "%~dp0"

echo ==========================================
echo   Extrator de Transcricao do YouTube
echo ==========================================
echo.

REM Verifica se o Python esta instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado no seu computador.
    echo Baixe e instale em: https://www.python.org/downloads/
    echo IMPORTANTE: marque a opcao "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

REM Verifica se a biblioteca necessaria esta instalada; se nao, instala
python -c "import youtube_transcript_api" >nul 2>nul
if %errorlevel% neq 0 (
    echo Instalando dependencia necessaria ^(youtube-transcript-api^)...
    python -m pip install youtube-transcript-api --quiet
    if %errorlevel% neq 0 (
        echo.
        echo [ERRO] Falha ao instalar a dependencia. Verifique sua conexao com a internet.
        pause
        exit /b 1
    )
    echo Instalacao concluida.
    echo.
)

echo Abrindo o aplicativo...
python youtube_transcript_app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] O aplicativo fechou com um erro. Veja a mensagem acima.
    pause
)
