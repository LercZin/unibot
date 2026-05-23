// =====================================================================
// Widget flutuante do UniBot
// Estado exposto globalmente em window.UniBotWidget.
// =====================================================================

(() => {
  const fab          = document.getElementById("unibot-fab");
  const widget       = document.getElementById("unibot-widget");
  const btnClose     = document.getElementById("unibot-close");
  const btnNova      = document.getElementById("unibot-new");
  const form         = document.getElementById("unibot-form");
  const input        = document.getElementById("unibot-text");
  const btnSend      = document.getElementById("unibot-send");
  const elMensagens  = document.getElementById("unibot-messages");
  const elSugestoes  = document.getElementById("unibot-suggestions");
  const chips        = document.querySelectorAll(".chip");

  let conversaId   = null;
  let aberto       = false;
  let historicoCarregado = false;

  // -------------------------------------------------------------------
  // UI
  // -------------------------------------------------------------------
  async function abrir() {
    widget.hidden = false;
    fab.style.display = "none";
    aberto = true;
    setTimeout(() => input.focus(), 50);
    if (!historicoCarregado) {
      await carregarHistorico();
      historicoCarregado = true;
    }
  }

  function fechar() {
    widget.hidden = true;
    fab.style.display = "inline-flex";
    aberto = false;
  }

  function abrirCom(pergunta) {
    abrir().then(() => {
      input.value = pergunta;
      setTimeout(() => form.dispatchEvent(new Event("submit", { cancelable: true })), 60);
    });
  }

  async function carregarHistorico() {
    // mostra skeleton enquanto carrega
    elMensagens.innerHTML = `
      <div class="bubble bot"><div class="skel skel-line medium"></div></div>
      <div class="bubble user" style="align-self:flex-end"><div class="skel skel-line short"></div></div>
      <div class="bubble bot"><div class="skel skel-line medium"></div></div>
    `;
    try {
      const msgs = await API.historico();
      elMensagens.innerHTML = "";
      if (msgs.length === 0) {
        adicionarBolha("bot", boasVindas());
      } else {
        msgs.forEach((m) => adicionarBolha(m.remetente, m.texto));
      }
    } catch (e) {
      elMensagens.innerHTML = "";
      adicionarBolha("bot", boasVindas());
    }
  }

  function boasVindas() {
    const nome = (TokenStore.user()?.nome || "").split(" ")[0];
    const ola = nome ? `Olá, ${nome}!` : "Olá!";
    return `${ola} 👋 Sou o **UniBot**. Posso ajudar com notas, prazos, boletos, declarações, calendário e muito mais. Manda uma pergunta!`;
  }

  function adicionarBolha(remetente, texto, extra = "") {
    const div = document.createElement("div");
    div.className = `bubble ${remetente} ${extra}`.trim();
    div.innerHTML = renderizar(texto);
    elMensagens.appendChild(div);
    elMensagens.scrollTop = elMensagens.scrollHeight;
    return div;
  }

  function adicionarTyping() {
    const div = document.createElement("div");
    div.className = "bubble bot thinking";
    div.innerHTML = `<div class="typing-dots"><span></span><span></span><span></span></div>`;
    elMensagens.appendChild(div);
    elMensagens.scrollTop = elMensagens.scrollHeight;
    return div;
  }

  /** Markdown leve. */
  function renderizar(texto) {
    const escaped = texto
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return escaped
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/(?<!\w)\*([^*]+)\*/g, "<em>$1</em>")
      .replace(/(https?:\/\/[^\s)]+)/g,
        '<a href="$1" target="_blank" rel="noopener">$1</a>');
  }

  // -------------------------------------------------------------------
  // Envio
  // -------------------------------------------------------------------
  async function enviar(texto) {
    adicionarBolha("usuario", texto);
    if (elSugestoes) elSugestoes.style.display = "none";
    input.value = "";
    btnSend.disabled = true;
    const ph = adicionarTyping();

    try {
      const r = await API.enviarMensagem(texto, conversaId);
      conversaId = r.conversa_id;
      ph.innerHTML = renderizar(r.resposta);
      ph.classList.remove("thinking");
    } catch (err) {
      ph.textContent = `Não consegui responder agora (${err.message}).`;
      ph.classList.remove("thinking");
    } finally {
      btnSend.disabled = false;
      input.focus();
    }
  }

  // -------------------------------------------------------------------
  // Eventos
  // -------------------------------------------------------------------
  function novaConversa() {
    conversaId = null;
    historicoCarregado = true;        // não buscar histórico antigo na nova conversa
    elMensagens.innerHTML = "";
    adicionarBolha("bot", boasVindas());
    if (elSugestoes) elSugestoes.style.display = "";
    input.focus();
  }

  fab.addEventListener("click", abrir);
  btnClose.addEventListener("click", fechar);
  btnNova?.addEventListener("click", novaConversa);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const texto = input.value.trim();
    if (texto) enviar(texto);
  });

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const msg = chip.dataset.msg;
      if (msg) enviar(msg);
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && aberto) fechar();
    // Ctrl/Cmd + K abre o UniBot
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      aberto ? input.focus() : abrir();
    }
  });

  // API pública
  window.UniBotWidget = { open: abrir, close: fechar, openWith: abrirCom };
})();
