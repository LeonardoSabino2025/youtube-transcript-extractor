#!/usr/bin/env python3
"""
YouTube Transcript Extractor - App local e 100% gratuito
-----------------------------------------------------------
Cole o link de um vídeo do YouTube e extraia a transcrição/legenda
diretamente, sem precisar de chave de API, servidor ou nuvem.

Requisitos (instalar uma vez):
    pip install youtube-transcript-api --break-system-packages

Como rodar:
    python3 youtube_transcript_app.py
"""

import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


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

    # Se já parece ser só o ID (11 caracteres, sem barras)
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", url_ou_id):
        return url_ou_id

    raise ValueError("Não consegui identificar o ID do vídeo nesse link.")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Extrator de Transcrição do YouTube")
        self.geometry("780x600")
        self.minsize(600, 450)

        self._montar_interface()

    def _montar_interface(self):
        pad = {"padx": 10, "pady": 6}

        topo = ttk.Frame(self)
        topo.pack(fill="x", **pad)

        ttk.Label(topo, text="Link do vídeo:").pack(side="left")
        self.entrada_url = ttk.Entry(topo)
        self.entrada_url.pack(side="left", fill="x", expand=True, padx=8)
        self.entrada_url.bind("<Return>", lambda e: self.buscar_transcricao())

        ttk.Label(topo, text="Idioma:").pack(side="left", padx=(8, 0))
        self.idioma_var = tk.StringVar(value="pt")
        combo_idioma = ttk.Combobox(
            topo, textvariable=self.idioma_var, width=6,
            values=["pt", "en", "es", "fr", "de", "it", "ja", "ko", "auto"],
        )
        combo_idioma.pack(side="left", padx=4)

        self.btn_buscar = ttk.Button(topo, text="Buscar", command=self.buscar_transcricao)
        self.btn_buscar.pack(side="left", padx=(8, 0))

        # Opções extras
        opcoes = ttk.Frame(self)
        opcoes.pack(fill="x", **pad)

        self.incluir_tempo = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            opcoes, text="Incluir marcação de tempo", variable=self.incluir_tempo
        ).pack(side="left")

        ttk.Button(opcoes, text="Salvar como .txt", command=self.salvar_txt).pack(side="right")
        ttk.Button(opcoes, text="Copiar tudo", command=self.copiar_tudo).pack(side="right", padx=6)

        # Área de texto
        area_frame = ttk.Frame(self)
        area_frame.pack(fill="both", expand=True, **pad)

        self.texto = tk.Text(area_frame, wrap="word", font=("Segoe UI", 10))
        scroll = ttk.Scrollbar(area_frame, command=self.texto.yview)
        self.texto.configure(yscrollcommand=scroll.set)
        self.texto.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Barra de status
        self.status_var = tk.StringVar(value="Pronto.")
        ttk.Label(self, textvariable=self.status_var, anchor="w").pack(fill="x", padx=10, pady=(0, 8))

    def buscar_transcricao(self):
        url = self.entrada_url.get().strip()
        if not url:
            messagebox.showwarning("Atenção", "Cole o link do vídeo primeiro.")
            return

        try:
            video_id = extrair_video_id(url)
        except ValueError as e:
            messagebox.showerror("Link inválido", str(e))
            return

        self.btn_buscar.config(state="disabled")
        self.status_var.set("Buscando transcrição...")
        self.texto.delete("1.0", "end")

        # Roda em thread separada pra não travar a interface
        threading.Thread(target=self._buscar_thread, args=(video_id,), daemon=True).start()

    def _buscar_thread(self, video_id: str):
        try:
            api = YouTubeTranscriptApi()
            idioma = self.idioma_var.get()

            if idioma == "auto":
                transcript_list = api.list(video_id)
                # pega a primeira disponível (gerada ou manual)
                transcript = next(iter(transcript_list))
                dados = transcript.fetch()
            else:
                try:
                    dados = api.fetch(video_id, languages=[idioma])
                except NoTranscriptFound:
                    # tenta achar qualquer idioma disponível e traduzir, se possível
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
                if self.incluir_tempo.get():
                    minutos = int(trecho.start // 60)
                    segundos = int(trecho.start % 60)
                    linhas.append(f"[{minutos:02d}:{segundos:02d}] {trecho.text}")
                else:
                    linhas.append(trecho.text)

            texto_final = "\n".join(linhas)
            self.after(0, self._exibir_resultado, texto_final)

        except TranscriptsDisabled:
            self.after(0, self._exibir_erro, "Esse vídeo não tem legendas/transcrição habilitadas.")
        except VideoUnavailable:
            self.after(0, self._exibir_erro, "Vídeo indisponível (removido, privado ou ID incorreto).")
        except NoTranscriptFound:
            self.after(0, self._exibir_erro, "Não encontrei transcrição nesse idioma para esse vídeo.")
        except Exception as e:
            self.after(0, self._exibir_erro, f"Erro inesperado: {e}")

    def _exibir_resultado(self, texto: str):
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", texto)
        self.status_var.set(f"Transcrição carregada ({len(texto.splitlines())} linhas).")
        self.btn_buscar.config(state="normal")

    def _exibir_erro(self, msg: str):
        self.status_var.set("Erro.")
        messagebox.showerror("Erro", msg)
        self.btn_buscar.config(state="normal")

    def salvar_txt(self):
        conteudo = self.texto.get("1.0", "end").strip()
        if not conteudo:
            messagebox.showwarning("Atenção", "Não há transcrição para salvar ainda.")
            return
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt")],
            initialfile="transcricao.txt",
        )
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)
            self.status_var.set(f"Salvo em: {caminho}")

    def copiar_tudo(self):
        conteudo = self.texto.get("1.0", "end").strip()
        if not conteudo:
            return
        self.clipboard_clear()
        self.clipboard_append(conteudo)
        self.status_var.set("Transcrição copiada para a área de transferência.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
