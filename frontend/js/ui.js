// ============================================================
// UI helpers: Toast, dropdown, hash router, skeletons
// ============================================================

// ---------- Toast ----------
const Toast = (() => {
  const container = document.getElementById("toasts");

  function show({ tipo = "info", titulo = "", mensagem, duracao = 4000 }) {
    const icones = {
      info:    "bi-info-circle-fill",
      success: "bi-check-circle-fill",
      warning: "bi-exclamation-triangle-fill",
      danger:  "bi-x-circle-fill",
    };
    const el = document.createElement("div");
    el.className = `toast ${tipo}`;
    el.innerHTML = `
      <i class="bi ${icones[tipo] || icones.info} toast-icon"></i>
      <div class="toast-body">
        ${titulo ? `<strong>${escapeHtml(titulo)}</strong>` : ""}
        ${escapeHtml(mensagem)}
      </div>
      <button class="toast-close" aria-label="Fechar"><i class="bi bi-x"></i></button>
    `;
    container.appendChild(el);
    const close = () => {
      el.classList.add("fade-out");
      setTimeout(() => el.remove(), 250);
    };
    el.querySelector(".toast-close").addEventListener("click", close);
    if (duracao > 0) setTimeout(close, duracao);
  }

  return {
    info:    (m, t) => show({ tipo: "info", mensagem: m, titulo: t }),
    success: (m, t) => show({ tipo: "success", mensagem: m, titulo: t }),
    warning: (m, t) => show({ tipo: "warning", mensagem: m, titulo: t }),
    danger:  (m, t) => show({ tipo: "danger", mensagem: m, titulo: t, duracao: 6000 }),
  };
})();

function escapeHtml(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ---------- Dropdown helper ----------
function bindDropdown({ trigger, menu, onOpen }) {
  const open = () => {
    menu.hidden = false;
    trigger.setAttribute("aria-expanded", "true");
    onOpen?.();
  };
  const close = () => {
    menu.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
  };
  const toggle = () => (menu.hidden ? open() : close());

  trigger.addEventListener("click", (e) => {
    e.stopPropagation();
    toggle();
  });
  document.addEventListener("click", (e) => {
    if (!menu.contains(e.target) && !trigger.contains(e.target)) close();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
  return { open, close, toggle };
}

// ---------- Hash router ----------
const HashRouter = (() => {
  const handlers = new Map();
  let fallbackHandler = null;

  function on(secao, handler) { handlers.set(secao, handler); }
  function fallback(handler) { fallbackHandler = handler; }

  /** Aceita "secao" ou "secao?param=valor". Devolve só a parte da rota. */
  function rotaDe(hash) {
    return (hash || "").split("?")[0];
  }

  function dispatch() {
    const secao = rotaDe(location.hash.slice(1)) || "inicio";
    const handler = handlers.get(secao);
    if (handler) handler();
    else if (fallbackHandler) fallbackHandler(secao);
  }

  function go(secao) {
    if (rotaDe(location.hash.slice(1)) === rotaDe(secao)) {
      // mesma rota base — força re-render
      dispatch();
    } else {
      location.hash = secao;
    }
  }
  window.addEventListener("hashchange", dispatch);
  function start() { dispatch(); }
  return { on, fallback, go, start };
})();

// ---------- Skeleton helpers ----------
const Skeleton = {
  cards(qtd = 4) {
    return Array.from({ length: qtd }, () => '<div class="skel skel-card"></div>').join("");
  },
  table(linhas = 3) {
    return `<table class="notas-table"><tbody>${
      Array.from({ length: linhas }, () => `
        <tr><td colspan="4"><div class="skel skel-line medium"></div></td></tr>
      `).join("")
    }</tbody></table>`;
  },
};

// Detecta 401 globais e exibe toast antes de redirecionar
window.addEventListener("unhandledrejection", (e) => {
  if (e.reason?.message === "Sessão expirada") {
    Toast.warning("Sua sessão expirou. Faça login novamente.", "Atenção");
  }
});
