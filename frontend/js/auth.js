if (TokenStore.get()) location.href = "portal.html";

const stepUsuario = document.querySelector('.form-step[data-step="1"]');
const stepSenha   = document.querySelector('.form-step[data-step="2"]');
const inputCpf    = document.getElementById("cpf");
const inputSenha  = document.getElementById("senha");
const chkLembrar  = document.getElementById("chk-lembrar");
const userDisplay = document.getElementById("user-display");
const btnAvancar  = document.getElementById("btn-avancar");
const btnVoltar   = document.getElementById("btn-voltar");
const btnEye      = document.getElementById("btn-toggle-senha");
const alerta      = document.getElementById("alerta");
const form        = document.getElementById("form-login");

// Pré-preenche com o último email/CPF usado
const ultimoEmail = TokenStore.lastEmail();
if (ultimoEmail) {
  inputCpf.value = ultimoEmail;
  // Se já temos email, pula direto pra senha
  setTimeout(() => btnAvancar.click(), 0);
}

btnAvancar.addEventListener("click", () => {
  const valor = inputCpf.value.trim();
  if (!valor) { inputCpf.focus(); return; }
  userDisplay.textContent = valor;
  stepUsuario.classList.add("d-none");
  stepSenha.classList.remove("d-none");
  inputSenha.focus();
});

btnVoltar.addEventListener("click", () => {
  alerta.classList.add("d-none");
  stepSenha.classList.add("d-none");
  stepUsuario.classList.remove("d-none");
  inputCpf.focus();
  inputCpf.select();
});

btnEye.addEventListener("click", () => {
  const t = inputSenha.type === "password" ? "text" : "password";
  inputSenha.type = t;
  btnEye.querySelector("i").className =
    t === "password" ? "bi bi-eye-slash" : "bi bi-eye";
});

inputCpf.addEventListener("keypress", (e) => {
  if (e.key === "Enter") { e.preventDefault(); btnAvancar.click(); }
});

// ---------- Modal "Esqueci minha senha" ----------
const linkEsqueci = document.getElementById("link-esqueci");
const modal       = document.getElementById("modal-recovery");
const recForm     = document.getElementById("form-recovery");
const recEmail    = document.getElementById("rec-email");
const recInfo     = document.getElementById("rec-info");
const recClose    = document.getElementById("rec-close");

function abrirModal() {
  recEmail.value = inputCpf.value.trim();
  recInfo.hidden = true;
  modal.hidden = false;
  setTimeout(() => recEmail.focus(), 50);
}
function fecharModal() { modal.hidden = true; }

linkEsqueci.addEventListener("click", (e) => { e.preventDefault(); abrirModal(); });
recClose.addEventListener("click", fecharModal);
modal.addEventListener("click", (e) => { if (e.target === modal) fecharModal(); });
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !modal.hidden) fecharModal();
});

recForm.addEventListener("submit", (e) => {
  e.preventDefault();
  recInfo.textContent =
    "Esta versão de demonstração não envia e-mails de recuperação. " +
    "Solicite ao responsável pelo ambiente a redefinição da conta.";
  recInfo.hidden = false;
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  alerta.classList.add("d-none");

  const usuario = inputCpf.value.trim();
  const senha   = inputSenha.value;
  const lembrar = chkLembrar.checked;

  // CPF de 11 dígitos vira o e-mail do seed (atalho de dev/demo)
  const apenasDigitos = usuario.replace(/\D/g, "");
  const ehCpf = /^\d{11}$/.test(apenasDigitos);
  const email = ehCpf ? "lucas@unibot.edu.br" : usuario;

  try {
    const r = await API.login(email, senha, lembrar);
    TokenStore.set(r.access_token, lembrar);
    TokenStore.setUser(r.usuario, lembrar);
    TokenStore.setLastEmail(usuario);   // sempre lembra o usuário, mesmo sem "lembrar-me"
    location.href = "portal.html";
  } catch (err) {
    alerta.textContent = err.message || "Não foi possível entrar.";
    alerta.classList.remove("d-none");
  }
});
