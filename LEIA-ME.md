# Extrator de Transcrição do YouTube — App Local Gratuito

App simples com interface gráfica que roda 100% no seu computador.
Sem servidor, sem nuvem, sem chave de API, sem custo.

## 1. Instalar o Python (se ainda não tiver)
Baixe em https://www.python.org/downloads/ (marque "Add Python to PATH" na instalação, no Windows).

## 2. Instalar a biblioteca necessária
Abra o terminal (cmd/PowerShell no Windows, Terminal no Mac/Linux) e rode:

```
pip install youtube-transcript-api
```

Se der erro de permissão no Linux/Mac, use:
```
pip install youtube-transcript-api --break-system-packages
```

## 3. Rodar o app
Na pasta onde salvou o arquivo `youtube_transcript_app.py`, rode:

```
python youtube_transcript_app.py
```

(No Mac/Linux pode ser `python3` em vez de `python`.)

## 4. Usar
1. Cole o link do vídeo (aceita link completo, link curto `youtu.be/...` ou de `/shorts/`).
2. Escolha o idioma da legenda (ex: `pt` para português, `en` para inglês, ou `auto` para pegar a primeira disponível).
3. Clique em **Buscar**.
4. Use **Copiar tudo** ou **Salvar como .txt** para exportar.

## Observações importantes
- Só funciona em vídeos que **tenham legenda** (manual ou automática) habilitada pelo criador/YouTube.
- Não baixa áudio nem vídeo — só o texto da legenda já existente.
- Se aparecer erro de "transcrição não encontrada" nesse idioma, tente `auto` — o app vai pegar a primeira legenda disponível.
- Como o app faz requisições diretas ao YouTube pela sua própria internet, ele pode eventualmente sofrer bloqueio temporário de IP se usado em excesso — isso é raro em uso pessoal normal.
