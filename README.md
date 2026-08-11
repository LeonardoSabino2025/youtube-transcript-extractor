# YouTube Transcript Extractor

App local e 100% gratuito para extrair a transcrição/legenda de vídeos do YouTube.
Sem servidor, sem nuvem, sem chave de API, sem custo — roda inteiramente no seu computador.

## ✨ Recursos

- Aceita link completo, link curto (`youtu.be/...`) ou de `/shorts/`
- Escolha do idioma da legenda (ou `auto` para pegar a primeira disponível)
- Marcação de tempo opcional (`[mm:ss]`)
- Copiar tudo ou salvar como `.txt`
- Interface gráfica simples (Tkinter — já vem com o Python)

## 🚀 Como usar (Windows)

1. Instale o [Python](https://www.python.org/downloads/) (marque **"Add Python to PATH"** na instalação)
2. Dê duplo clique em **`iniciar_app.bat`**
   - Ele instala a dependência automaticamente na primeira vez e já abre o app

## 🚀 Como usar (Mac/Linux)

```bash
pip install youtube-transcript-api
python3 youtube_transcript_app.py
```

## ⚠️ Observações

- Só funciona em vídeos que tenham legenda (manual ou automática) habilitada.
- Não baixa áudio nem vídeo — apenas o texto da legenda já existente.
- Consulte [`LEIA-ME.md`](LEIA-ME.md) para o passo a passo detalhado.
