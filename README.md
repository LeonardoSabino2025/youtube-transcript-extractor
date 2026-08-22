# YouTube Transcript Extractor

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://extrator-transcricao-youtube.streamlit.app)

Extrai a transcrição/legenda de vídeos do YouTube. Sem chave de API, sem custo.
Disponível em três versões: desktop (Tkinter), web local (Flask) e web na nuvem (Streamlit).

## ✨ Recursos

- Aceita link completo, link curto (`youtu.be/...`) ou de `/shorts/`
- Escolha do idioma da legenda (ou `auto` para pegar a primeira disponível)
- Marcação de tempo opcional (`[mm:ss]`)
- Copiar tudo ou salvar como `.txt`
- Busca automática do título do vídeo

## 🖥️ Versão desktop (Tkinter)

```bash
pip install youtube-transcript-api
python youtube_transcript_app.py
```

No Windows, dê duplo clique em **`iniciar_app.bat`** (instala a dependência automaticamente).

## 🌐 Versão web local (Flask)

```bash
pip install -r requirements.txt
python app_web.py
```

Acesse `http://localhost:5000`. No Windows, dê duplo clique em **`iniciar_app_web.bat`**.

## ☁️ Versão Streamlit (deploy na nuvem)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Pronta para publicar no [Streamlit Community Cloud](https://streamlit.io/cloud):
1. Conecte este repositório em share.streamlit.io
2. Defina `streamlit_app.py` como arquivo principal
3. Deploy

## 🚫 Bloqueio de IP pelo YouTube (nuvem)

O YouTube bloqueia com frequência os IPs compartilhados de provedores de nuvem
(Streamlit Community Cloud incluso). Quando isso acontece, o app mostra um erro
avisando que é bloqueio temporário — não é um problema com o vídeo em si nem
com o código. A própria biblioteca `youtube-transcript-api` recomenda usar um
proxy residencial rotativo para contornar isso.

Se o bloqueio for frequente, configure um proxy definindo variáveis de
ambiente (ou Secrets, no Streamlit Cloud):

**Opção 1 — Webshare (recomendado pela biblioteca):**
```
WEBSHARE_PROXY_USERNAME=<seu usuário>
WEBSHARE_PROXY_PASSWORD=<sua senha>
```
Crie uma conta em [webshare.io](https://www.webshare.io/) (plano "Residential"
ou "Static Residential"), pegue as credenciais do proxy e cole-as em
**App settings → Secrets** no Streamlit Cloud (formato `CHAVE = "valor"`, uma
por linha) — nunca no código ou no repositório.

**Opção 2 — outro provedor de proxy:**
```
GENERIC_PROXY_HTTP_URL=http://usuario:senha@host:porta
GENERIC_PROXY_HTTPS_URL=https://usuario:senha@host:porta
```

Sem nenhuma dessas variáveis definidas, o app funciona normalmente sem proxy
(como hoje) — elas são totalmente opcionais.

## 🧩 Estrutura

- `transcript_core.py` — lógica de extração compartilhada por todas as versões
- `youtube_transcript_app.py` — versão desktop (Tkinter)
- `app_web.py` + `templates/` + `static/` — versão web local (Flask)
- `streamlit_app.py` — versão web na nuvem (Streamlit)

## ⚠️ Observações

- Só funciona em vídeos que tenham legenda (manual ou automática) habilitada.
- Não baixa áudio nem vídeo — apenas o texto da legenda já existente.
- O YouTube pode bloquear temporariamente requisições em excesso vindas do mesmo IP (mais comum em servidores na nuvem).
- Consulte [`LEIA-ME.md`](LEIA-ME.md) para o passo a passo detalhado da versão desktop.
