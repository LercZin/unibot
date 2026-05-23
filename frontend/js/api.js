const API_BASE = (() => {
  if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
    return "http://localhost:8000/api";
  }
  return "/api";
})();

/**
 * TokenStore — busca o token em localStorage (lembrar-me ON) ou
 * sessionStorage (lembrar-me OFF). Em `set` o chamador decide onde gravar.
 * Em `get` consulta ambos, dando preferência ao persistente.
 */
const TokenStore = {
  get: () =>
    localStorage.getItem("unibot_token") ||
    sessionStorage.getItem("unibot_token"),

  set: (token, persistir = true) => {
    const target = persistir ? localStorage : sessionStorage;
    const other  = persistir ? sessionStorage : localStorage;
    target.setItem("unibot_token", token);
    other.removeItem("unibot_token");
  },

  drop: () => {
    localStorage.removeItem("unibot_token");
    sessionStorage.removeItem("unibot_token");
    localStorage.removeItem("unibot_user");
    sessionStorage.removeItem("unibot_user");
  },

  user: () => {
    const raw = localStorage.getItem("unibot_user") ||
                sessionStorage.getItem("unibot_user");
    return raw ? JSON.parse(raw) : null;
  },

  setUser: (u, persistir = true) => {
    const target = persistir ? localStorage : sessionStorage;
    const other  = persistir ? sessionStorage : localStorage;
    target.setItem("unibot_user", JSON.stringify(u));
    other.removeItem("unibot_user");
  },

  // Email do último login bem-sucedido — sempre em localStorage.
  lastEmail: () => localStorage.getItem("unibot_last_email") || "",
  setLastEmail: (e) => localStorage.setItem("unibot_last_email", e),
};

async function apiFetch(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = TokenStore.get();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const resp = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (resp.status === 401) {
    if (!path.startsWith("/auth/")) {
      TokenStore.drop();
      // Deixa o toast aparecer antes de redirecionar
      if (typeof Toast !== "undefined") {
        Toast.warning("Sua sessão expirou. Redirecionando para o login...", "Atenção");
        setTimeout(() => (location.href = "index.html"), 1500);
      } else {
        location.href = "index.html";
      }
    }
    throw new Error("Sessão expirada");
  }
  if (!resp.ok) {
    const corpo = await resp.json().catch(() => ({}));
    throw new Error(corpo.mensagem || `Erro ${resp.status}`);
  }
  return resp.status === 204 ? null : resp.json();
}

const API = {
  login: (email, senha, lembrar = false) =>
    apiFetch("/auth/login", { method: "POST",
      body: JSON.stringify({ email, senha, lembrar }) }),
  enviarMensagem: (texto, conversa_id = null) =>
    apiFetch("/chat/mensagens", { method: "POST", body: JSON.stringify({ texto, conversa_id }) }),
  historico: (conversa_id = null) =>
    apiFetch(`/chat/historico${conversa_id ? `?conversa_id=${conversa_id}` : ""}`),
  minhasDisciplinas: () => apiFetch("/disciplinas/minhas"),
  proximosPrazos:    () => apiFetch("/prazos/proximos"),
  desempenho:    (disciplinaId) => apiFetch(`/notas/desempenho/${disciplinaId}`),

  // Documentos do aluno
  historico:   () => apiFetch("/aluno/historico"),
  atestado:    () => apiFetch("/aluno/atestado"),
  carteirinha: () => apiFetch("/aluno/carteirinha"),
};
