from datetime import datetime

from app.db.repositories.base_conhecimento_repo import BaseConhecimentoRepository
from app.db.repositories.conversa_repo import ConversaRepository
from app.db.repositories.disciplina_repo import DisciplinaRepository
from app.db.repositories.faq_repo import FaqRepository
from app.db.repositories.nota_repo import NotaRepository
from app.db.repositories.prazo_repo import PrazoRepository
from app.domain.conversa import IntencaoMensagem, Remetente
from app.domain.nota import calcular_media_ponderada, classificar_situacao
from app.domain.usuario import Estudante
from app.services.claude_service import ClaudeService
from app.services.processador_nlp import ProcessadorNLP

_SYSTEM_BASE = """Você é o UniBot, um assistente acadêmico da Anhanguera.
Responda em português brasileiro, de forma direta, didática e amigável.
Use os dados de contexto fornecidos. Quando não souber, admita; não invente
prazos, notas ou conteúdos.
"""

# Intenções resolvidas direto pela tabela `faq_institucional`, sem ir no Claude.
_INTENCOES_FAQ_PURAS = {
    IntencaoMensagem.FAQ_FINANCEIRO,
    IntencaoMensagem.FAQ_HISTORICO,
    IntencaoMensagem.FAQ_DECLARACAO_MATRICULA,
    IntencaoMensagem.FAQ_CALENDARIO,
    IntencaoMensagem.FAQ_RENOVACAO,
    IntencaoMensagem.FAQ_TRANCAMENTO,
    IntencaoMensagem.FAQ_LOGIN,
    IntencaoMensagem.FAQ_ESTAGIO,
    IntencaoMensagem.FAQ_TCC,
    IntencaoMensagem.FAQ_DIPLOMA,
    IntencaoMensagem.FAQ_SECRETARIA,
}


class Chatbot:
    """Núcleo do chatbot híbrido do UniBot.

    Fluxo:
    1) Identifica a intenção via ProcessadorNLP.
    2) Para intenções administrativas (FAQ institucional), responde
       direto da tabela `faq_institucional` — rápido, barato e confiável.
    3) Para CONSULTA_NOTA/PRAZO, monta o resumo a partir dos dados reais
       do estudante (com fallback de FAQ quando não houver disciplina alvo).
    4) Para tudo o mais (DUVIDA_CONTEUDO, GERAR_RESUMO, ...), delega ao
       Claude com um system prompt enriquecido.
    """

    def __init__(
        self,
        *,
        nlp: ProcessadorNLP | None = None,
        claude: ClaudeService | None = None,
        conversa_repo: ConversaRepository | None = None,
        disciplina_repo: DisciplinaRepository | None = None,
        prazo_repo: PrazoRepository | None = None,
        nota_repo: NotaRepository | None = None,
        bc_repo: BaseConhecimentoRepository | None = None,
        faq_repo: FaqRepository | None = None,
    ) -> None:
        self._nlp = nlp or ProcessadorNLP()
        self._claude = claude  # instanciação preguiçosa
        self._conversa_repo = conversa_repo or ConversaRepository()
        self._disciplina_repo = disciplina_repo or DisciplinaRepository()
        self._prazo_repo = prazo_repo or PrazoRepository()
        self._nota_repo = nota_repo or NotaRepository()
        self._bc_repo = bc_repo or BaseConhecimentoRepository()
        self._faq_repo = faq_repo or FaqRepository()

    # ------------------------------------------------------------------ #
    # Ponto de entrada
    # ------------------------------------------------------------------ #
    def responder(self, estudante: Estudante, mensagem: str, conversa_id: int | None = None) -> dict:
        intencao = self._nlp.identificar_intencao(mensagem)
        conv_id = self._conversa_repo.resolver_do_usuario(estudante.id, conversa_id)

        self._conversa_repo.adicionar_mensagem(
            conversa_id=conv_id, usuario_id=estudante.id, remetente=Remetente.USUARIO,
            texto=mensagem, intencao=intencao,
        )

        if intencao == IntencaoMensagem.SAUDACAO:
            texto, tokens = self._responder_saudacao(estudante), 0
        elif intencao in _INTENCOES_FAQ_PURAS:
            texto, tokens = self._responder_faq(intencao, mensagem), 0
        elif intencao == IntencaoMensagem.CONSULTA_NOTA:
            texto, tokens = self._responder_consulta_nota(estudante, mensagem)
        elif intencao == IntencaoMensagem.CONSULTA_PRAZO:
            texto, tokens = self._responder_consulta_prazo(estudante), 0
        elif intencao == IntencaoMensagem.OUTRO:
            # Antes de gastar tokens no Claude, tenta achar algo na FAQ
            texto_faq = self._tentar_faq_global(mensagem)
            if texto_faq is not None:
                texto, tokens = texto_faq, 0
            else:
                texto, tokens = self._responder_via_claude(estudante, mensagem, intencao, conv_id)
        else:
            texto, tokens = self._responder_via_claude(estudante, mensagem, intencao, conv_id)

        self._conversa_repo.adicionar_mensagem(
            conversa_id=conv_id, usuario_id=estudante.id, remetente=Remetente.BOT,
            texto=texto, intencao=intencao, tokens_usados=tokens,
        )
        return {
            "conversa_id": conv_id,
            "intencao": intencao.value,
            "resposta": texto,
            "tokens": tokens,
        }

    # ------------------------------------------------------------------ #
    # Handlers determinísticos
    # ------------------------------------------------------------------ #
    def _responder_saudacao(self, estudante: Estudante) -> str:
        return (
            f"Olá, {estudante.nome.split()[0]}! 👋 Eu sou o UniBot. "
            "Posso te ajudar com **notas**, **prazos**, **boletos**, **histórico**, "
            "**declaração de matrícula**, **calendário acadêmico**, **rematrícula**, "
            "**trancamento**, **estágio**, **TCC**, **diploma** e muito mais. "
            "Como posso ajudar?"
        )

    def _responder_faq(self, intencao: IntencaoMensagem, mensagem: str) -> str:
        categoria = intencao.categoria_faq
        if categoria is None:
            return "Não consegui identificar o assunto. Pode reformular?"
        item = self._faq_repo.melhor_match(categoria, mensagem)
        if item is None:
            return "Ainda não tenho essa informação cadastrada. Procure a secretaria."
        return item.formatar()

    def _tentar_faq_global(self, mensagem: str) -> str | None:
        """Busca termo em TODA a FAQ. Retorna a melhor resposta se houver
        match com score útil; senão None pra cair no Claude."""
        itens = self._faq_repo.buscar_global(mensagem, limite=1)
        return itens[0].formatar() if itens else None

    def _responder_consulta_prazo(self, estudante: Estudante) -> str:
        prazos = self._prazo_repo.listar_proximos_do_estudante(estudante.id, limite=5)
        if not prazos:
            return "Você não tem prazos cadastrados no horizonte próximo. 🎉"
        linhas = ["📅 **Próximos prazos:**", ""]
        for p in prazos:
            linhas.append(f"• **{p.titulo}** ({p.tipo.value}) — {p.data_entrega:%d/%m/%Y às %H:%M}")
        return "\n".join(linhas)

    def _responder_consulta_nota(self, estudante: Estudante, mensagem: str) -> tuple[str, int]:
        disciplinas = self._disciplina_repo.listar_do_estudante(estudante.id)
        nomes = [d.nome for d in disciplinas]
        alvo = self._nlp.extrair_disciplina_mencionada(mensagem, nomes)

        # Pergunta genérica (sem disciplina) → FAQ "como vejo minhas notas"
        if alvo is None:
            item = self._faq_repo.melhor_match("notas", mensagem)
            if item:
                if disciplinas:
                    extra = "Suas disciplinas: " + ", ".join(nomes) + "."
                    return (item.formatar() + "\n\n" + extra, 0)
                return (item.formatar(), 0)
            return ("Sobre qual disciplina você quer saber? " + ", ".join(nomes), 0)

        disc = next(d for d in disciplinas if d.nome == alvo)
        notas = self._nota_repo.listar_do_estudante_em_disciplina(estudante.id, disc.id)
        if not notas:
            return (f"Ainda não há notas lançadas em **{disc.nome}**.", 0)

        media = calcular_media_ponderada(notas)
        situacao = classificar_situacao(media)
        linhas = [f"📊 **{disc.nome}**", ""]
        for n in notas:
            linhas.append(f"• {n.tipo}: **{n.valor}** (peso {n.peso})")
        linhas.append("")
        linhas.append(f"Média parcial: **{media}** — situação: **{situacao}**.")
        return ("\n".join(linhas), 0)

    # ------------------------------------------------------------------ #
    # Fallback para Claude
    # ------------------------------------------------------------------ #
    def _responder_via_claude(self, estudante: Estudante, mensagem: str,
                              intencao: IntencaoMensagem, conv_id: int) -> tuple[str, int]:
        if self._claude is None:
            self._claude = ClaudeService()

        disciplinas = self._disciplina_repo.listar_do_estudante(estudante.id)
        nomes = [d.nome for d in disciplinas]
        alvo = self._nlp.extrair_disciplina_mencionada(mensagem, nomes)

        contexto = [
            f"Estudante: {estudante.nome} (matrícula {estudante.matricula}, "
            f"{estudante.curso}, {estudante.semestre}º semestre).",
            f"Disciplinas matriculadas: {', '.join(nomes) if nomes else 'nenhuma'}.",
            f"Data/hora atual: {datetime.now():%d/%m/%Y %H:%M}.",
        ]
        if alvo and intencao == IntencaoMensagem.DUVIDA_CONTEUDO:
            disc = next(d for d in disciplinas if d.nome == alvo)
            itens = self._bc_repo.buscar_por_termo(disc.id, mensagem, limite=3)
            if itens:
                contexto.append(f"Trechos da base de conhecimento de {disc.nome}:")
                for it in itens:
                    contexto.append(f"### {it.topico}\n{it.conteudo}")

        historico = [
            {"role": "user" if m.remetente == Remetente.USUARIO else "assistant",
             "content": m.texto}
            for m in self._conversa_repo.listar_mensagens(conv_id, limite=10, usuario_id=estudante.id)[:-1]
        ]

        resp = self._claude.gerar_resposta(
            system_prompt=_SYSTEM_BASE + "\n\n" + "\n".join(contexto),
            historico=historico,
            mensagem_usuario=mensagem,
        )
        return resp.texto, resp.total_tokens
