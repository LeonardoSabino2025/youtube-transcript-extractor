#!/usr/bin/env python3
"""
Extrator de Transcrição do YouTube - Versão Web
--------------------------------------------------
Mesma lógica do app original (Tkinter), agora servida como app web local
via Flask, para acesso pelo navegador.

Requisitos (instalar uma vez):
    pip install flask youtube-transcript-api

Como rodar:
    python app_web.py

Depois acesse no navegador: http://localhost:5000
"""

from flask import Flask, jsonify, render_template, request

from transcript_core import (
    NoTranscriptFound,
    RequestBlocked,
    TranscriptsDisabled,
    VideoUnavailable,
    buscar_transcricao,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/transcricao", methods=["POST"])
def api_transcricao():
    payload = request.get_json(silent=True) or {}
    url = (payload.get("url") or "").strip()
    idioma = (payload.get("idioma") or "pt").strip()
    incluir_tempo = bool(payload.get("incluir_tempo", True))

    if not url:
        return jsonify({"erro": "Cole o link do vídeo primeiro."}), 400

    try:
        resultado = buscar_transcricao(url, idioma=idioma, incluir_tempo=incluir_tempo)
        return jsonify(resultado)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except TranscriptsDisabled:
        return jsonify({"erro": "Esse vídeo não tem legendas/transcrição habilitadas."}), 422
    except VideoUnavailable:
        return jsonify({"erro": "Vídeo indisponível (removido, privado ou ID incorreto)."}), 422
    except NoTranscriptFound:
        return jsonify({"erro": "Não encontrei transcrição nesse idioma para esse vídeo."}), 422
    except RequestBlocked:
        return jsonify({
            "erro": (
                "O YouTube bloqueou temporariamente as requisições vindas deste "
                "servidor (bloqueio de IP de nuvem). Tente novamente em alguns "
                "minutos ou configure um proxy — veja o README do projeto."
            )
        }), 503
    except Exception as e:
        return jsonify({"erro": f"Erro inesperado: {e}"}), 500


if __name__ == "__main__":
    print("Abrindo em: http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
