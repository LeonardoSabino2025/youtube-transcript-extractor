const urlInput = document.getElementById("urlInput");
const idiomaSelect = document.getElementById("idiomaSelect");
const incluirTempo = document.getElementById("incluirTempo");
const btnBuscar = document.getElementById("btnBuscar");
const btnCopiar = document.getElementById("btnCopiar");
const btnSalvar = document.getElementById("btnSalvar");
const resultado = document.getElementById("resultado");
const status = document.getElementById("status");

async function buscarTranscricao() {
  const url = urlInput.value.trim();
  if (!url) {
    status.textContent = "Cole o link do vídeo primeiro.";
    return;
  }

  btnBuscar.disabled = true;
  status.textContent = "Buscando transcrição...";
  resultado.value = "";

  try {
    const resp = await fetch("/api/transcricao", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url,
        idioma: idiomaSelect.value,
        incluir_tempo: incluirTempo.checked,
      }),
    });

    const dados = await resp.json();

    if (!resp.ok) {
      status.textContent = "Erro.";
      alert(dados.erro || "Erro desconhecido.");
      return;
    }

    resultado.value = dados.texto;
    status.textContent = `Transcrição carregada (${dados.total_linhas} linhas).`;
  } catch (err) {
    status.textContent = "Erro.";
    alert("Erro de conexão com o servidor: " + err);
  } finally {
    btnBuscar.disabled = false;
  }
}

function copiarTudo() {
  const conteudo = resultado.value.trim();
  if (!conteudo) return;
  navigator.clipboard.writeText(conteudo).then(() => {
    status.textContent = "Transcrição copiada para a área de transferência.";
  });
}

function salvarTxt() {
  const conteudo = resultado.value.trim();
  if (!conteudo) {
    alert("Não há transcrição para salvar ainda.");
    return;
  }
  const blob = new Blob([conteudo], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "transcricao.txt";
  link.click();
  URL.revokeObjectURL(link.href);
  status.textContent = "Transcrição baixada como transcricao.txt";
}

btnBuscar.addEventListener("click", buscarTranscricao);
btnCopiar.addEventListener("click", copiarTudo);
btnSalvar.addEventListener("click", salvarTxt);
urlInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") buscarTranscricao();
});
