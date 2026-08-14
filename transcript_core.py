"""Lógica compartilhada de extração de transcrição do YouTube.

Usada tanto pela versão Flask (app_web.py) quanto pela versão Streamlit
(streamlit_app.py).
"""

import json
import re
import urllib.parse
import urllib.request

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

__all__ = [
    "extrair_video_id",
    "buscar_titulo_video",
    "buscar_transcricao",
    "TranscriptsDisabled",
    "VideoUnavailable",
    "NoTranscriptFound",
]


def extrair_video_id(url_ou_id: str) -> str:
    """Aceita link completo, link curto (youtu.be) ou apenas o ID e devolve o ID."""
    url_ou_id = url_ou_id.strip()

    padroes = [
        r"(?:v=|\/videos\/|embed\/|youtu\.be\/|\/v\/|\/shorts\/)([0-9A-Za-z_-]{11})",
    ]
    for padrao in padroes:
        m = re.search(padrao, url_ou_id)
        if m:
            return m.group(1)

    if re.fullmatch(r"[0-9A-Za-z_-]{11}", url_ou_id):
        return url_ou_id

    raise ValueError("Não consegui identificar o ID do vídeo nesse link.")


def buscar_titulo_video(video_id: str) -> str:
    """Busca o título do vídeo via endpoint público oEmbed do YouTube (sem chave de API)."""
    url_video = f"https://www.youtube.com/watch?v={video_id}"
    oembed_url = "https://www.youtube.com/oembed?" + urllib.parse.urlencode(
        {"url": url_video, "format": "json"}
    )
    try:
        with urllib.request.urlopen(oembed_url, timeout=8) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
            return dados.get("title", "").strip()
    except Exception:
        return ""


def buscar_transcricao(url: str, idioma: str = "pt", incluir_tempo: bool = True) -> dict:
    """Extrai a transcrição de um vídeo do YouTube.

    Retorna um dict com: titulo, link, texto, total_linhas.
    Propaga TranscriptsDisabled, VideoUnavailable, NoTranscriptFound e ValueError.
    """
    video_id = extrair_video_id(url)

    api = YouTubeTranscriptApi()

    if idioma == "auto":
        transcript_list = api.list(video_id)
        transcript = next(iter(transcript_list))
        dados = transcript.fetch()
    else:
        try:
            dados = api.fetch(video_id, languages=[idioma])
        except NoTranscriptFound:
            transcript_list = api.list(video_id)
            disponiveis = list(transcript_list)
            if not disponiveis:
                raise
            primeira = disponiveis[0]
            if primeira.is_translatable:
                dados = primeira.translate(idioma).fetch()
            else:
                dados = primeira.fetch()

    linhas = []
    for trecho in dados:
        if incluir_tempo:
            minutos = int(trecho.start // 60)
            segundos = int(trecho.start % 60)
            linhas.append(f"[{minutos:02d}:{segundos:02d}] {trecho.text}")
        else:
            linhas.append(trecho.text)

    titulo = buscar_titulo_video(video_id)
    link_video = f"https://www.youtube.com/watch?v={video_id}"

    cabecalho = []
    if titulo:
        cabecalho.append(f"Título: {titulo}")
    cabecalho.append(f"Link: {link_video}")
    cabecalho.append("-" * 40)

    texto_final = "\n".join(cabecalho) + "\n\n" + "\n".join(linhas)

    return {
        "titulo": titulo,
        "link": link_video,
        "texto": texto_final,
        "total_linhas": len(linhas),
    }
