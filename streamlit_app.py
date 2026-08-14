#!/usr/bin/env python3
"""
Extrator de Transcrição do YouTube - Versão Streamlit
--------------------------------------------------------
App pronto para rodar localmente (`streamlit run streamlit_app.py`) ou
publicado no Streamlit Community Cloud (share.streamlit.io).
"""

import streamlit as st

from transcript_core import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    buscar_transcricao,
)

st.set_page_config(page_title="Extrator de Transcrição do YouTube", page_icon="🎬", layout="centered")

st.title("🎬 Extrator de Transcrição do YouTube")
st.caption("Cole o link de um vídeo e extraia a transcrição/legenda, sem chave de API.")

if "texto_resultado" not in st.session_state:
    st.session_state.texto_resultado = ""
if "nome_arquivo" not in st.session_state:
    st.session_state.nome_arquivo = "transcricao.txt"

with st.form("form_busca"):
    col_url, col_idioma = st.columns([3, 1])
    with col_url:
        url = st.text_input("Link do vídeo", placeholder="https://www.youtube.com/watch?v=...")
    with col_idioma:
        idioma = st.selectbox(
            "Idioma", ["pt", "en", "es", "fr", "de", "it", "ja", "ko", "auto"], index=0
        )

    incluir_tempo = st.checkbox("Incluir marcação de tempo", value=True)
    enviado = st.form_submit_button("Buscar", type="primary")

if enviado:
    if not url.strip():
        st.warning("Cole o link do vídeo primeiro.")
    else:
        with st.spinner("Buscando transcrição..."):
            try:
                resultado = buscar_transcricao(url, idioma=idioma, incluir_tempo=incluir_tempo)
                st.session_state.texto_resultado = resultado["texto"]
                titulo_slug = (resultado["titulo"] or "transcricao").strip()[:60]
                st.session_state.nome_arquivo = f"{titulo_slug or 'transcricao'}.txt"
                st.success(f"Transcrição carregada ({resultado['total_linhas']} linhas).")
            except ValueError as e:
                st.error(str(e))
            except TranscriptsDisabled:
                st.error("Esse vídeo não tem legendas/transcrição habilitadas.")
            except VideoUnavailable:
                st.error("Vídeo indisponível (removido, privado ou ID incorreto).")
            except NoTranscriptFound:
                st.error("Não encontrei transcrição nesse idioma para esse vídeo.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")

if st.session_state.texto_resultado:
    st.text_area("Resultado", value=st.session_state.texto_resultado, height=400)
    st.download_button(
        "Salvar como .txt",
        data=st.session_state.texto_resultado,
        file_name=st.session_state.nome_arquivo,
        mime="text/plain",
    )
