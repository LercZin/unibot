if (!TokenStore.get()) location.href = "index.html";

const usuario   = TokenStore.user();
const elContent = document.getElementById("section-content");
const navItems  = document.querySelectorAll(".nav-item");

// ============================================================
// User dropdown
// ============================================================
const chipNome  = document.getElementById("chip-nome");
const menuNome  = document.getElementById("menu-nome");
const menuEmail = document.getElementById("menu-email");
if (usuario) {
  chipNome.textContent  = (usuario.nome || "").split(" ").slice(0, 2).join(" ");
  menuNome.textContent  = usuario.nome;
  menuEmail.textContent = usuario.email;
}

const userDD = bindDropdown({
  trigger: document.getElementById("btn-user-menu"),
  menu:    document.getElementById("user-menu"),
});

document.querySelectorAll(".user-menu-item").forEach((b) => {
  b.addEventListener("click", () => {
    userDD.close();
    const acao = b.dataset.action;
    if (acao === "sair") {
      TokenStore.drop();
      localStorage.removeItem("unibot_user");
      Toast.success("Você saiu do portal.");
      setTimeout(() => (location.href = "index.html"), 600);
    } else if (acao === "perfil") {
      Toast.info("Página de perfil ainda em construção.");
    } else if (acao === "config") {
      Toast.info("Configurações ainda em construção.");
    }
  });
});

// ============================================================
// Topbar: dropdown de notificações + ações
// ============================================================
const NOTIFICACOES = [
  { id: 1, tipo: "warning", icone: "calendar-event", titulo: "Prova de POO II",
    msg: "Quarta-feira, 28/05 às 19h", tempo: "em 5 dias", lida: false },
  { id: 2, tipo: "info", icone: "file-earmark-check", titulo: "Histórico solicitado",
    msg: "Está em processamento (5 dias úteis)", tempo: "há 2 dias", lida: false },
  { id: 3, tipo: "success", icone: "check-circle", titulo: "Boleto pago",
    msg: "Mensalidade de maio confirmada", tempo: "há 5 dias", lida: false },
];

function renderNotificacoes() {
  const list = document.getElementById("notif-list");
  const badge = document.getElementById("notif-badge");
  const naoLidas = NOTIFICACOES.filter((n) => !n.lida).length;
  badge.textContent = naoLidas;
  badge.style.display = naoLidas > 0 ? "" : "none";

  if (NOTIFICACOES.length === 0) {
    list.innerHTML = `<div class="notif-empty">Nenhuma notificação no momento.</div>`;
    return;
  }
  list.innerHTML = NOTIFICACOES.map((n) => `
    <div class="notif-item ${n.tipo} ${n.lida ? "" : "unread"}" data-id="${n.id}">
      <span class="notif-icon"><i class="bi bi-${n.icone}"></i></span>
      <div class="notif-body">
        <strong>${escapeHtml(n.titulo)}</strong>
        <p>${escapeHtml(n.msg)}</p>
        <time>${escapeHtml(n.tempo)}</time>
      </div>
    </div>
  `).join("");

  list.querySelectorAll(".notif-item").forEach((el) => {
    el.addEventListener("click", () => {
      const n = NOTIFICACOES.find((x) => x.id === Number(el.dataset.id));
      if (n) n.lida = true;
      renderNotificacoes();
      Toast.info(n?.titulo || "Notificação");
    });
  });
}
renderNotificacoes();

const notifDD = bindDropdown({
  trigger: document.getElementById("btn-notif"),
  menu:    document.getElementById("notif-menu"),
});

document.getElementById("notif-mark-read")?.addEventListener("click", (e) => {
  e.stopPropagation();
  NOTIFICACOES.forEach((n) => (n.lida = true));
  renderNotificacoes();
});

document.getElementById("btn-avisos")?.addEventListener("click",
  () => Toast.info("Não há avisos publicados no momento.", "Avisos"));
document.getElementById("btn-config")?.addEventListener("click",
  () => Toast.info("Configurações ainda em construção."));
document.getElementById("btn-abrir-chat")?.addEventListener("click",
  () => window.UniBotWidget?.open());

// ============================================================
// Sidebar mobile (drawer)
// ============================================================
const sidebar         = document.getElementById("sidebar");
const sidebarBackdrop = document.getElementById("sidebar-backdrop");
const btnHamb         = document.getElementById("btn-hamburger");
const btnSidebarClose = document.getElementById("btn-sidebar-close");

function abrirSidebar() {
  sidebar.classList.add("open");
  sidebarBackdrop.classList.add("show");
}
function fecharSidebar() {
  sidebar.classList.remove("open");
  sidebarBackdrop.classList.remove("show");
}
btnHamb?.addEventListener("click", abrirSidebar);
btnSidebarClose?.addEventListener("click", fecharSidebar);
sidebarBackdrop?.addEventListener("click", fecharSidebar);

// Busca da topbar — envia direto pro UniBot
const searchInput = document.getElementById("search-portal");
searchInput?.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    const q = searchInput.value.trim();
    if (!q) return;
    window.UniBotWidget?.openWith(q);
    searchInput.value = "";
  }
});

// ============================================================
// Navegação por hash (refresh-safe)
// ============================================================
const SECOES = ["inicio", "meu-curso", "financeiro", "notas",
                "secretaria", "solicitacoes", "estudar"];

navItems.forEach((item) => {
  item.addEventListener("click", () => {
    // O <a href="#xxx"> já muda o hash; fechamos só o drawer no mobile.
    fecharSidebar();
  });
});

function ativar(secao) {
  navItems.forEach((n) =>
    n.classList.toggle("active", n.dataset.section === secao));
  elContent.scrollTop = 0;
}

HashRouter.on("inicio",       () => { ativar("inicio");       renderInicio();      });
HashRouter.on("meu-curso",    () => { ativar("meu-curso");    renderMeuCurso();    });
HashRouter.on("financeiro",   () => { ativar("financeiro");   renderFinanceiro();  });
HashRouter.on("notas",        () => { ativar("meu-curso");    renderNotas();       });
HashRouter.on("secretaria",   () => { ativar("secretaria");   renderSecretaria();  });
HashRouter.on("solicitacoes", () => { ativar("solicitacoes"); renderSolicitacoes();});
HashRouter.on("estudar",      () => { ativar("estudar");      renderEstudar();     });
HashRouter.on("historico",    () => { ativar("secretaria");   renderHistorico();   });
HashRouter.on("atestado",     () => { ativar("secretaria");   renderAtestado();    });
HashRouter.on("carteirinha",  () => { ativar("secretaria");   renderCarteirinha(); });
HashRouter.on("horarios",     () => { ativar("meu-curso");    renderHorarios();    });

HashRouter.fallback((rotaDesconhecida) => {
  elContent.innerHTML = `
    <h1 class="greeting">Página não encontrada</h1>
    <p class="greeting-sub">
      Não existe nada em <code>#${escapeHtml(rotaDesconhecida)}</code>.
    </p>
    <div class="cards-grid">
      ${cardHTML("house-door", "blue", "Voltar para o Início", "Levar pra dashboard", "go-home")}
    </div>
  `;
  document.querySelector('[data-jump="go-home"]')
    ?.addEventListener("click", () => HashRouter.go("inicio"));
});

// ============================================================
// Seção: Início
// ============================================================
async function renderInicio() {
  const primeiroNome = (usuario?.nome || "aluno").split(" ")[0];
  elContent.innerHTML = `
    <h1 class="greeting">Olá, ${primeiroNome}</h1>
    <p class="greeting-sub">
      Boas-vindas ao Portal do Aluno!
      Aqui você encontra as ferramentas necessárias para acompanhar sua trajetória acadêmica.
    </p>

    <div class="unibot-banner">
      <img src="img/unibot-logo.svg" alt="UniBot" />
      <div>
        <h3>Precisa de algo? Pergunte ao UniBot</h3>
        <p>Notas, boletos, declarações, calendário — tudo em segundos por mensagem.</p>
      </div>
      <button id="open-unibot-from-banner">Abrir chat</button>
    </div>

    <h2 class="section-title">Acesso rápido</h2>
    <div class="cards-grid">
      ${cardHTML("calendar3",      "blue",   "Quadro de Horários", "Acompanhe o horário das suas aulas", "horarios")}
      ${cardHTML("bookmark",       "purple", "Disciplinas e Notas","Acompanhe suas disciplinas e notas", "notas")}
      ${cardHTML("play-circle",    "green",  "Estudar",            "Acesse seu AVA", "estudar")}
      ${cardHTML("question-circle","orange", "Dúvidas e Orientações","Falar com o UniBot", "ask-unibot")}
    </div>

    <h2 class="section-title">Tarefas importantes</h2>
    <div class="task-list" id="task-list">
      ${taskItemHTML("file-earmark-check","green","Entregar documentos","Parabéns, você entregou todos os documentos.",100)}
      ${taskItemHTML("award","orange","Atividades complementares","Entregue suas atividades complementares",60,"warn")}
      <div class="task-item" data-task="proximas">
        <span class="icon-circle blue"><i class="bi bi-calendar-event"></i></span>
        <div class="task-body">
          <h4>Próximas avaliações</h4>
          <div class="skel skel-line medium"></div>
        </div>
        <i class="bi bi-chevron-right chev"></i>
      </div>
    </div>
  `;

  document.getElementById("open-unibot-from-banner")
    ?.addEventListener("click", () => window.UniBotWidget?.open());

  document.querySelector('[data-jump="notas"]')
    ?.addEventListener("click", () => HashRouter.go("notas"));
  document.querySelector('[data-jump="estudar"]')
    ?.addEventListener("click", () => HashRouter.go("estudar"));
  document.querySelector('[data-jump="horarios"]')
    ?.addEventListener("click", () => HashRouter.go("horarios"));
  document.querySelector('[data-jump="ask-unibot"]')
    ?.addEventListener("click", () => window.UniBotWidget?.open());

  try {
    const prazos = await API.proximosPrazos();
    const body = document.querySelector('[data-task="proximas"] .task-body');
    if (!body) return;
    if (prazos.length === 0) {
      body.innerHTML = `<h4>Próximas avaliações</h4><p>Sem prazos pendentes 🎉</p>`;
    } else {
      const top = prazos.slice(0, 2)
        .map((p) => `${p.titulo} (${new Date(p.data_entrega).toLocaleDateString("pt-BR")})`)
        .join(" · ");
      body.innerHTML = `
        <h4>Próximas avaliações</h4>
        <p>${prazos.length} prazo(s) próximos: ${top}</p>`;
    }
  } catch (e) {
    const body = document.querySelector('[data-task="proximas"] .task-body');
    if (body) body.innerHTML = `<h4>Próximas avaliações</h4><p>Não foi possível carregar.</p>`;
  }
}

function cardHTML(icone, cor, titulo, descricao, jumpTo = null) {
  const data = jumpTo ? `data-jump="${jumpTo}"` : "";
  return `
    <div class="card-quick" ${data}>
      <span class="icon-circle ${cor}"><i class="bi bi-${icone}"></i></span>
      <div>
        <h3>${titulo}</h3>
        <p>${descricao}</p>
      </div>
    </div>`;
}

function taskItemHTML(icone, cor, titulo, descricao, percent, klass = "") {
  return `
    <div class="task-item">
      <span class="icon-circle ${cor}"><i class="bi bi-${icone}"></i></span>
      <div class="task-body">
        <h4>${titulo}</h4>
        <p>${descricao}</p>
        <div class="progress ${klass}"><span style="width:${percent}%"></span></div>
      </div>
      <i class="bi bi-chevron-right chev"></i>
    </div>`;
}

// ============================================================
// Seção: Meu Curso
// ============================================================
async function renderMeuCurso() {
  elContent.innerHTML = `
    <h1 class="greeting">Meu Curso</h1>
    <p class="greeting-sub">Suas disciplinas matriculadas neste semestre.</p>
    <div class="cards-grid" id="disc-grid">${Skeleton.cards(3)}</div>`;

  try {
    const disciplinas = await API.minhasDisciplinas();
    const grid = document.getElementById("disc-grid");
    if (disciplinas.length === 0) {
      grid.innerHTML = `<p>Você ainda não tem disciplinas matriculadas.</p>`;
      return;
    }
    grid.innerHTML = disciplinas.map((d) => `
      <div class="card-quick" data-disc-id="${d.id}">
        <span class="icon-circle purple"><i class="bi bi-journal-bookmark"></i></span>
        <div>
          <h3>${escapeHtml(d.nome)}</h3>
          <p>${d.codigo} · ${d.carga_horaria}h</p>
        </div>
      </div>`).join("");

    grid.querySelectorAll("[data-disc-id]").forEach((el) => {
      el.addEventListener("click", () => {
        location.hash = `notas?disc=${el.dataset.discId}`;
      });
    });
  } catch (e) {
    document.getElementById("disc-grid").innerHTML =
      `<p>Erro ao carregar: ${escapeHtml(e.message)}</p>`;
    Toast.danger("Não foi possível carregar suas disciplinas.");
  }
}

// ============================================================
// Seção: Notas
// ============================================================
async function renderNotas() {
  // suporta hash do tipo "notas?disc=1"
  const queryDisc = new URLSearchParams(location.hash.split("?")[1] || "").get("disc");

  elContent.innerHTML = `
    <h1 class="greeting">Disciplinas e Notas</h1>
    <p class="greeting-sub">Selecione uma disciplina para ver suas notas e a situação atual.</p>
    <div id="notas-disc-grid" class="cards-grid">${Skeleton.cards(3)}</div>
    <div id="notas-detalhes"></div>
  `;

  let disciplinas = [];
  try {
    disciplinas = await API.minhasDisciplinas();
  } catch (e) {
    Toast.danger("Não foi possível carregar suas disciplinas.");
    document.getElementById("notas-disc-grid").innerHTML =
      `<p>Erro ao carregar.</p>`;
    return;
  }

  const grid = document.getElementById("notas-disc-grid");
  if (disciplinas.length === 0) {
    grid.innerHTML = `<p>Você ainda não tem disciplinas matriculadas.</p>`;
    return;
  }
  grid.innerHTML = disciplinas.map((d) => `
    <div class="card-quick" data-disc-id="${d.id}">
      <span class="icon-circle purple"><i class="bi bi-journal-bookmark"></i></span>
      <div>
        <h3>${escapeHtml(d.nome)}</h3>
        <p>${d.codigo}</p>
      </div>
    </div>`).join("");

  grid.querySelectorAll("[data-disc-id]").forEach((el) =>
    el.addEventListener("click", () => {
      grid.querySelectorAll(".card-quick").forEach((c) => c.classList.remove("is-active"));
      el.classList.add("is-active");
      mostrarDesempenho(Number(el.dataset.discId), disciplinas);
    }));

  // pré-seleção via query
  const inicial = queryDisc ? Number(queryDisc) : disciplinas[0].id;
  const inicialEl = grid.querySelector(`[data-disc-id="${inicial}"]`);
  inicialEl?.classList.add("is-active");
  mostrarDesempenho(inicial, disciplinas);
}

async function mostrarDesempenho(discId, disciplinas) {
  const detalhes = document.getElementById("notas-detalhes");
  const disc = disciplinas.find((d) => d.id === discId);
  detalhes.innerHTML = `
    <h2 class="section-title" style="margin-top:1.5rem">${escapeHtml(disc?.nome || "")}</h2>
    ${Skeleton.table()}
  `;
  try {
    const d = await API.desempenho(discId);
    if (d.notas.length === 0) {
      detalhes.innerHTML = `
        <h2 class="section-title" style="margin-top:1.5rem">${escapeHtml(d.disciplina_nome)}</h2>
        <p>Ainda não há notas lançadas em ${escapeHtml(d.disciplina_nome)}.</p>`;
      return;
    }
    detalhes.innerHTML = `
      <h2 class="section-title" style="margin-top:1.5rem">${escapeHtml(d.disciplina_nome)}</h2>
      <table class="notas-table">
        <thead>
          <tr><th>Avaliação</th><th>Nota</th><th>Peso</th><th>Data</th></tr>
        </thead>
        <tbody>
          ${d.notas.map((n) => `
            <tr>
              <td>${escapeHtml(n.tipo)}</td>
              <td><strong>${n.valor}</strong></td>
              <td>${n.peso}</td>
              <td>${new Date(n.data).toLocaleDateString("pt-BR")}</td>
            </tr>`).join("")}
        </tbody>
      </table>
      <div style="display:flex; gap:1rem; align-items:center; margin-bottom:1.5rem;">
        <span>Média parcial: <strong>${d.media}</strong></span>
        <span class="situacao-pill ${d.situacao}">${d.situacao.replace("_", " ")}</span>
      </div>
    `;
  } catch (e) {
    detalhes.innerHTML = `<p>Erro ao carregar notas: ${escapeHtml(e.message)}</p>`;
  }
}

// ============================================================
// Seção: Financeiro
// ============================================================
function renderFinanceiro() {
  elContent.innerHTML = `
    <h1 class="greeting">Financeiro</h1>
    <p class="greeting-sub">Boletos, mensalidades e situação financeira.</p>

    <div class="unibot-banner">
      <img src="img/unibot-logo.svg" alt="UniBot" />
      <div>
        <h3>Dúvidas sobre pagamentos?</h3>
        <p>Pergunte ao UniBot — "como emito um boleto?", "quando vence?", "estou inadimplente"...</p>
      </div>
      <button onclick="window.UniBotWidget?.open()">Abrir chat</button>
    </div>

    <div class="cards-grid">
      ${cardHTML("receipt", "blue",          "2ª via de boleto",     "Emita seus boletos",         "ask-boleto")}
      ${cardHTML("calendar-check", "green",  "Próximos vencimentos", "Veja suas próximas datas",   "ask-vencimento")}
      ${cardHTML("currency-exchange","orange","Negociação",          "Negocie débitos em atraso",  "ask-inadimplente")}
      ${cardHTML("file-earmark-text","purple","Extrato financeiro",  "Histórico de pagamentos",    "ask-extrato")}
    </div>
  `;
  document.querySelector('[data-jump="ask-boleto"]')
    ?.addEventListener("click", () => window.UniBotWidget?.openWith("Como emito um boleto?"));
  document.querySelector('[data-jump="ask-vencimento"]')
    ?.addEventListener("click", () => window.UniBotWidget?.openWith("Quando vence meu pagamento?"));
  document.querySelector('[data-jump="ask-inadimplente"]')
    ?.addEventListener("click", () => window.UniBotWidget?.openWith("Estou inadimplente, o que faço?"));
  document.querySelector('[data-jump="ask-extrato"]')
    ?.addEventListener("click", () => window.UniBotWidget?.openWith("Onde vejo meu extrato financeiro?"));
}

// ============================================================
// Seção: Secretaria
// ============================================================
function renderSecretaria() {
  elContent.innerHTML = `
    <h1 class="greeting">Secretaria</h1>
    <p class="greeting-sub">O que você deseja solicitar?</p>

    <div class="tabs" id="tabs-sec">
      <button class="active" data-tab="recomendacoes">
        <i class="bi bi-stars"></i> Recomendações
      </button>
      <button data-tab="academicos">
        <i class="bi bi-mortarboard"></i> Acadêmicos
      </button>
      <button data-tab="financeiros">
        <i class="bi bi-cash-coin"></i> Financeiros
      </button>
    </div>

    <div class="cards-grid">
      ${cardHTML("person-vcard",     "blue",   "Carteirinha Digital",      "Sua identificação estudantil", "ask-carteirinha")}
      ${cardHTML("file-earmark-text","purple", "Atestado de Matrícula",    "Comprovante para banco, INSS, etc.", "ask-atestado")}
      ${cardHTML("journal-text",     "green",  "Histórico Escolar",        "Documento das disciplinas cursadas", "ask-historico")}
      ${cardHTML("award",            "orange", "Atividades complementares","Entrega e validação")}
    </div>

    <h2 class="section-title">Dúvidas Frequentes</h2>
    <div class="cards-grid">
      ${cardHTML("chat-dots", "blue",  "TCC e Estágio",  "Orientador, normas, vagas...",   "ask-academico")}
      ${cardHTML("chat-dots", "purple","Renovação e Trancamento", "Como pausar ou continuar", "ask-renovacao")}
    </div>
  `;

  document.querySelectorAll("#tabs-sec button").forEach((b) =>
    b.addEventListener("click", () => {
      document.querySelectorAll("#tabs-sec button").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
    })
  );

  document.querySelector('[data-jump="ask-carteirinha"]')
    ?.addEventListener("click", () => HashRouter.go("carteirinha"));
  document.querySelector('[data-jump="ask-atestado"]')
    ?.addEventListener("click", () => HashRouter.go("atestado"));
  document.querySelector('[data-jump="ask-historico"]')
    ?.addEventListener("click", () => HashRouter.go("historico"));
  document.querySelector('[data-jump="ask-academico"]')
    ?.addEventListener("click", () => window.UniBotWidget?.openWith("Preciso de informações sobre o TCC"));
  document.querySelector('[data-jump="ask-renovacao"]')
    ?.addEventListener("click", () => window.UniBotWidget?.openWith("Como renovo minha matrícula?"));
}

// ============================================================
// Seções stub
// ============================================================
function renderSolicitacoes() {
  elContent.innerHTML = `
    <h1 class="greeting">Minhas Solicitações</h1>
    <p class="greeting-sub">Acompanhe o status das suas solicitações abertas.</p>
    <div class="task-list">
      ${taskItemHTML("hourglass-split","orange","Atestado de Matrícula","Em processamento — previsão: hoje",70,"warn")}
      ${taskItemHTML("check-circle","green","Histórico Escolar","Concluído em 14/04/2026",100)}
    </div>
  `;
}

function renderEstudar() {
  elContent.innerHTML = `
    <h1 class="greeting">Estudar</h1>
    <p class="greeting-sub">Acesse o AVA para conteúdos, vídeos e atividades das disciplinas.</p>
    <div class="cards-grid">
      ${cardHTML("play-btn", "blue",      "Abrir o AVA",      "Conteúdos e atividades")}
      ${cardHTML("book",     "purple",    "Biblioteca virtual","Livros e artigos")}
      ${cardHTML("question-circle","green","Dúvidas no chat",  "Tire dúvidas com o UniBot", "ask-content")}
    </div>
  `;
  document.querySelector('[data-jump="ask-content"]')
    ?.addEventListener("click", () =>
      window.UniBotWidget?.openWith("Explica o conceito de polimorfismo em POO"));
}

// ============================================================
// Seção: Histórico Escolar (documento)
// ============================================================
async function renderHistorico() {
  elContent.innerHTML = docToolbarHTML("Histórico Escolar") +
    `<div class="document" id="doc-area">${Skeleton.table(4)}</div>`;
  ligarToolbar();

  try {
    const h = await API.historico();
    const area = document.getElementById("doc-area");
    const dt   = new Date(h.emitido_em);
    area.innerHTML = `
      ${docHeaderHTML("Histórico Escolar", h.codigo_verificacao)}
      ${docAlunoInfoHTML(h.aluno)}

      <h3 class="doc-section-title">Disciplinas cursadas</h3>
      <table class="doc-table">
        <thead>
          <tr>
            <th>Período</th><th>Código</th><th>Disciplina</th>
            <th class="num">CH</th><th class="num">Média</th><th>Situação</th>
          </tr>
        </thead>
        <tbody>
          ${h.matriculas.map((m) => `
            <tr>
              <td>${escapeHtml(m.periodo)}</td>
              <td>${escapeHtml(m.codigo)}</td>
              <td>${escapeHtml(m.nome)}</td>
              <td class="num">${m.carga_horaria}h</td>
              <td class="num">${m.notas.length ? m.media : "—"}</td>
              <td><span class="situacao-pill ${m.situacao}">
                ${m.situacao.replace("_", " ")}
              </span></td>
            </tr>`).join("")}
        </tbody>
        <tfoot>
          <tr>
            <td colspan="3">Total aprovado: ${h.total_aprovadas} de ${h.total_disciplinas} disciplina(s)</td>
            <td class="num">${h.carga_horaria_aprovada}h</td>
            <td colspan="2"></td>
          </tr>
        </tfoot>
      </table>

      <div class="doc-signature">
        <div class="line"></div>
        <p><strong>UniBot · Secretaria Acadêmica</strong></p>
      </div>

      ${docFooterHTML(dt, h.codigo_verificacao)}
    `;
  } catch (e) {
    document.getElementById("doc-area").innerHTML =
      `<p>Erro ao carregar o histórico: ${escapeHtml(e.message)}</p>`;
    Toast.danger("Não foi possível carregar seu histórico.");
  }
}

// ============================================================
// Seção: Atestado de Matrícula (documento)
// ============================================================
async function renderAtestado() {
  elContent.innerHTML = docToolbarHTML("Atestado de Matrícula") +
    `<div class="document" id="doc-area">${Skeleton.table(3)}</div>`;
  ligarToolbar();

  try {
    const a = await API.atestado();
    const dt = new Date(a.emitido_em);
    const venc = new Date(dt);
    venc.setDate(venc.getDate() + a.validade_dias);

    const disciplinasUL = a.disciplinas_matriculadas.length === 0
      ? "<li>Nenhuma disciplina ativa neste período.</li>"
      : a.disciplinas_matriculadas
          .map((d) => `<li><strong>${escapeHtml(d.codigo)}</strong> — ${escapeHtml(d.nome)} (${d.carga_horaria}h)</li>`)
          .join("");

    document.getElementById("doc-area").innerHTML = `
      ${docHeaderHTML("Atestado de Matrícula", a.codigo_verificacao)}

      <p class="doc-paragraph">
        Atesto, para os devidos fins, que
        <strong>${escapeHtml(a.aluno.nome)}</strong>,
        portador(a) da matrícula <strong>${escapeHtml(a.aluno.matricula)}</strong>,
        está regularmente matriculado(a) no curso de
        <strong>${escapeHtml(a.aluno.curso)}</strong>,
        cursando o <strong>${a.aluno.semestre}º semestre</strong>
        no período letivo <strong>${escapeHtml(a.periodo_letivo)}</strong>
        nesta instituição.
      </p>

      <h3 class="doc-section-title">Disciplinas matriculadas no período ${escapeHtml(a.periodo_letivo)}</h3>
      <ul style="line-height: 1.8; padding-left: 1.25rem;">${disciplinasUL}</ul>

      <p class="doc-paragraph" style="margin-top:1.5rem">
        Este documento tem validade de <strong>${a.validade_dias} dias</strong>
        a partir da data de emissão, vencendo em
        <strong>${venc.toLocaleDateString("pt-BR")}</strong>.
      </p>

      <div class="doc-signature">
        <div class="line"></div>
        <p><strong>UniBot · Secretaria Acadêmica</strong></p>
        <p style="color: var(--c-muted); font-size: .8rem; margin-top: .25rem;">
          Documento emitido digitalmente — não requer assinatura física.
        </p>
      </div>

      ${docFooterHTML(dt, a.codigo_verificacao)}
    `;
  } catch (e) {
    document.getElementById("doc-area").innerHTML =
      `<p>Erro ao carregar o atestado: ${escapeHtml(e.message)}</p>`;
    Toast.danger("Não foi possível gerar o atestado.");
  }
}

// ============================================================
// Seção: Carteirinha Digital
// ============================================================
async function renderCarteirinha() {
  elContent.innerHTML = docToolbarHTML("Carteirinha Digital") +
    `<div id="doc-area" style="display:flex; justify-content:center;">
       <div class="skel" style="width:360px; height:340px; border-radius:18px"></div>
     </div>`;
  ligarToolbar();

  try {
    const c = await API.carteirinha();
    const venc = new Date(c.validade);
    const iniciais = c.aluno.nome.split(" ")
      .filter(Boolean).slice(0, 2)
      .map((p) => p[0]).join("").toUpperCase();

    document.getElementById("doc-area").innerHTML = `
      <div class="carteirinha">
        <div class="cart-head">
          <img src="img/unibot-logo.svg" alt="UniBot" />
          <div>
            <span class="label">Carteirinha do Estudante</span>
          </div>
        </div>
        <div class="cart-avatar">${escapeHtml(iniciais)}</div>
        <p class="cart-nome">${escapeHtml(c.aluno.nome)}</p>
        <p class="cart-curso">${escapeHtml(c.aluno.curso)} · ${c.aluno.semestre}º semestre</p>
        <div class="cart-info">
          <div>
            <span class="label">Matrícula</span>
            <strong>${escapeHtml(c.aluno.matricula)}</strong>
          </div>
          <div>
            <span class="label">Validade</span>
            <strong>${venc.toLocaleDateString("pt-BR")}</strong>
          </div>
        </div>
        <p class="cart-qr">${escapeHtml(c.qr_codigo)}</p>
      </div>
    `;
  } catch (e) {
    Toast.danger("Não foi possível carregar sua carteirinha.");
  }
}

// ============================================================
// Seção: Quadro de Horários (gerado a partir das disciplinas matriculadas)
// ============================================================
async function renderHorarios() {
  elContent.innerHTML = `
    <h1 class="greeting">Quadro de Horários</h1>
    <p class="greeting-sub">Horário das suas aulas neste semestre.</p>
    ${Skeleton.cards(3)}`;

  let disciplinas;
  try {
    disciplinas = await API.minhasDisciplinas();
  } catch (e) {
    elContent.innerHTML += `<p>Erro ao carregar.</p>`;
    return;
  }

  // Distribui cada disciplina em slots fixos, deterministicamente pelo id.
  const DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"];
  const SLOTS = [
    { ini: "19:00", fim: "20:40" },
    { ini: "20:50", fim: "22:30" },
  ];
  const CORES = ["blue", "purple", "green", "orange"];

  const grade = {};
  DIAS.forEach((d) => { grade[d] = {}; SLOTS.forEach((s) => grade[d][s.ini] = null); });

  disciplinas.forEach((d, i) => {
    // mantém aulas duas vezes na semana, padrão Mon/Wed ou Tue/Thu
    const offset = i % 2;
    const slot = SLOTS[i % SLOTS.length];
    grade[DIAS[offset]][slot.ini]     = { ...d, slot, cor: CORES[i % CORES.length] };
    grade[DIAS[offset + 2]][slot.ini] = { ...d, slot, cor: CORES[i % CORES.length] };
  });

  let tabelaHTML = `<table class="doc-table" style="margin-top:1rem">
    <thead><tr>
      <th>Horário</th>${DIAS.map((d) => `<th>${d}</th>`).join("")}
    </tr></thead><tbody>`;
  SLOTS.forEach((s) => {
    tabelaHTML += `<tr>
      <td><strong>${s.ini}<br>${s.fim}</strong></td>
      ${DIAS.map((dia) => {
        const aula = grade[dia][s.ini];
        if (!aula) return `<td style="color: var(--c-muted)">—</td>`;
        return `<td>
          <div class="icon-circle ${aula.cor}" style="display:inline-flex; width:24px; height:24px; font-size:.75rem">
            <i class="bi bi-bookmark-fill"></i>
          </div>
          <strong>${escapeHtml(aula.codigo)}</strong><br>
          <span style="font-size:.85rem; color:var(--c-muted)">${escapeHtml(aula.nome)}</span>
        </td>`;
      }).join("")}
    </tr>`;
  });
  tabelaHTML += `</tbody></table>`;

  elContent.innerHTML = `
    <h1 class="greeting">Quadro de Horários</h1>
    <p class="greeting-sub">Horário das suas aulas neste semestre.</p>
    ${tabelaHTML}
  `;
}

// ============================================================
// Helpers de documento
// ============================================================
function docToolbarHTML(titulo) {
  return `
    <div class="doc-toolbar">
      <div>
        <a href="#secretaria" style="font-size:.9rem">← Voltar para Secretaria</a>
        <h1 class="greeting" style="margin-top:.25rem">${escapeHtml(titulo)}</h1>
      </div>
      <div class="actions">
        <button class="btn-doc" id="btn-print">
          <i class="bi bi-printer"></i> Imprimir / Salvar PDF
        </button>
      </div>
    </div>`;
}
function ligarToolbar() {
  document.getElementById("btn-print")?.addEventListener("click", () => window.print());
}
function docHeaderHTML(titulo, codigo) {
  return `
    <header class="doc-header">
      <img src="img/unibot-logo.svg" alt="UniBot" />
      <div class="doc-title">
        <h1>${escapeHtml(titulo)}</h1>
        <h2>UniBot · Sistema Acadêmico</h2>
      </div>
      <div class="doc-code">
        Documento: ${escapeHtml(codigo)}
      </div>
    </header>`;
}
function docAlunoInfoHTML(aluno) {
  return `
    <dl class="doc-aluno-info">
      <dt>Nome:</dt>      <dd>${escapeHtml(aluno.nome)}</dd>
      <dt>Matrícula:</dt> <dd>${escapeHtml(aluno.matricula)}</dd>
      <dt>Curso:</dt>     <dd>${escapeHtml(aluno.curso)}</dd>
      <dt>Semestre:</dt>  <dd>${aluno.semestre}º</dd>
    </dl>`;
}
function docFooterHTML(dataEmissao, codigo) {
  return `
    <footer class="doc-footer">
      <div>
        Emitido em ${dataEmissao.toLocaleDateString("pt-BR")}
        às ${dataEmissao.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}
      </div>
      <div>Código de verificação: ${escapeHtml(codigo)}</div>
    </footer>`;
}

// ============================================================
// Boot
// ============================================================
HashRouter.start("inicio");
