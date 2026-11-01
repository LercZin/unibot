"""Testes do orquestrador Chatbot.

Mocka os repositórios e o ClaudeService para validar APENAS o roteamento:
- FAQ pura responde direto da tabela (0 tokens)
- consulta_nota/prazo monta a resposta com dados reais
- DUVIDA_CONTEUDO delega ao Claude
- OUTRO tenta fallback FAQ global antes do Claude
"""
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.domain.conversa import IntencaoMensagem, Remetente
from app.domain.disciplina import Disciplina
from app.domain.faq import FaqItem
from app.domain.nota import Nota
from app.domain.prazo import Prazo, TipoPrazo
from app.domain.usuario import Estudante
from app.services.chatbot import Chatbot


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def estudante():
    return Estudante(
        id=1, nome="Lucas Carvalho", email="lucas@unibot.edu.br",
        senha_hash="h", data_cadastro=datetime(2026, 1, 1), ativo=True,
        matricula="2025001", curso="ADS", semestre=4,
    )


@pytest.fixture
def chatbot():
    """Chatbot com TODAS as dependências mockadas."""
    conversa_repo = MagicMock()
    conversa_repo.buscar_ou_criar_ativa.return_value = 42
    conversa_repo.resolver_do_usuario.return_value = 42
    conversa_repo.adicionar_mensagem.return_value = 100
    conversa_repo.listar_mensagens.return_value = []

    disciplina_repo = MagicMock()
    disciplina_repo.listar_do_estudante.return_value = [
        Disciplina(id=1, codigo="POO2", nome="Programação Orientada a Objetos II",
                   carga_horaria=80, ementa="", professor_id=3),
    ]

    prazo_repo = MagicMock()
    nota_repo = MagicMock()
    bc_repo = MagicMock()
    faq_repo = MagicMock()
    claude = MagicMock()

    bot = Chatbot(
        conversa_repo=conversa_repo,
        disciplina_repo=disciplina_repo,
        prazo_repo=prazo_repo,
        nota_repo=nota_repo,
        bc_repo=bc_repo,
        faq_repo=faq_repo,
        claude=claude,
    )
    return bot


# ---------------------------------------------------------------------------
# Saudação
# ---------------------------------------------------------------------------
def test_saudacao_responde_sem_chamar_claude(chatbot, estudante):
    r = chatbot.responder(estudante, "Oi!")
    assert r["intencao"] == IntencaoMensagem.SAUDACAO.value
    assert r["tokens"] == 0
    assert "Lucas" in r["resposta"]
    chatbot._claude.gerar_resposta.assert_not_called()


# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
def test_faq_financeiro_responde_da_tabela(chatbot, estudante):
    chatbot._faq_repo.melhor_match.return_value = FaqItem(
        id=1, categoria="financeiro",
        pergunta="Como emito boleto?",
        resposta="Acesse Portal > Financeiro > 2ª via.",
        link="https://portal/x",
    )
    r = chatbot.responder(estudante, "Como emito um boleto?")
    assert r["intencao"] == IntencaoMensagem.FAQ_FINANCEIRO.value
    assert r["tokens"] == 0
    assert "Acesse Portal" in r["resposta"]
    assert "https://portal/x" in r["resposta"]
    chatbot._faq_repo.melhor_match.assert_called_once_with(
        "financeiro", "Como emito um boleto?"
    )
    chatbot._claude.gerar_resposta.assert_not_called()


def test_faq_sem_resultado_devolve_mensagem_padrao(chatbot, estudante):
    chatbot._faq_repo.melhor_match.return_value = None
    r = chatbot.responder(estudante, "Como emito um boleto?")
    assert r["tokens"] == 0
    assert "secretaria" in r["resposta"].lower()


# ---------------------------------------------------------------------------
# Consulta nota
# ---------------------------------------------------------------------------
def test_consulta_nota_com_disciplina_alvo(chatbot, estudante):
    chatbot._nota_repo.listar_do_estudante_em_disciplina.return_value = [
        Nota(id=1, matricula_id=1, tipo="AV1", valor=Decimal("8.0"),
             peso=Decimal("1.0"), data=date(2026, 4, 10)),
        Nota(id=2, matricula_id=1, tipo="AV2", valor=Decimal("7.0"),
             peso=Decimal("1.0"), data=date(2026, 4, 25)),
    ]
    r = chatbot.responder(estudante, "como estou em Programação Orientada a Objetos II?")
    assert r["intencao"] == IntencaoMensagem.CONSULTA_NOTA.value
    assert r["tokens"] == 0
    assert "AV1" in r["resposta"] and "AV2" in r["resposta"]
    assert "7.50" in r["resposta"]  # média = (8+7)/2
    assert "aprovado" in r["resposta"]
    chatbot._claude.gerar_resposta.assert_not_called()


def test_consulta_nota_sem_disciplina_cai_no_faq(chatbot, estudante):
    chatbot._faq_repo.melhor_match.return_value = FaqItem(
        id=10, categoria="notas",
        pergunta="Como vejo minhas notas?",
        resposta="Pergunte aqui mesmo ou veja no Portal.",
    )
    r = chatbot.responder(estudante, "como vejo minhas notas?")
    assert r["intencao"] == IntencaoMensagem.CONSULTA_NOTA.value
    assert r["tokens"] == 0
    assert "Pergunte aqui mesmo" in r["resposta"]


# ---------------------------------------------------------------------------
# Consulta prazo
# ---------------------------------------------------------------------------
def test_consulta_prazo_lista_proximos(chatbot, estudante):
    chatbot._prazo_repo.listar_proximos_do_estudante.return_value = [
        Prazo(id=1, disciplina_id=1, titulo="Prova bimestral",
              descricao="", tipo=TipoPrazo.PROVA,
              data_entrega=datetime(2026, 5, 28, 19, 0)),
    ]
    r = chatbot.responder(estudante, "qual a próxima prova?")
    assert r["intencao"] == IntencaoMensagem.CONSULTA_PRAZO.value
    assert r["tokens"] == 0
    assert "Prova bimestral" in r["resposta"]


# ---------------------------------------------------------------------------
# Conteúdo didático → Claude
# ---------------------------------------------------------------------------
def test_duvida_conteudo_delega_ao_claude(chatbot, estudante):
    from app.services.claude_service import RespostaClaude
    chatbot._claude.gerar_resposta.return_value = RespostaClaude(
        texto="Polimorfismo é...", tokens_entrada=50, tokens_saida=80,
    )
    chatbot._bc_repo.buscar_por_termo.return_value = []
    r = chatbot.responder(estudante, "Explica polimorfismo em Programação Orientada a Objetos II")
    assert r["intencao"] == IntencaoMensagem.DUVIDA_CONTEUDO.value
    assert r["tokens"] == 130
    assert "Polimorfismo" in r["resposta"]
    chatbot._claude.gerar_resposta.assert_called_once()


# ---------------------------------------------------------------------------
# OUTRO → fallback FAQ global antes do Claude
# ---------------------------------------------------------------------------
def test_outro_tenta_faq_global_antes_do_claude(chatbot, estudante):
    chatbot._faq_repo.buscar_global.return_value = [
        FaqItem(id=99, categoria="diploma",
                pergunta="ENADE?", resposta="ENADE é obrigatório...", link=None),
    ]
    r = chatbot.responder(estudante, "alguma coisa estranha aqui")
    assert r["intencao"] == IntencaoMensagem.OUTRO.value
    assert r["tokens"] == 0
    assert "ENADE" in r["resposta"]
    chatbot._claude.gerar_resposta.assert_not_called()


def test_outro_sem_faq_cai_no_claude(chatbot, estudante):
    from app.services.claude_service import RespostaClaude
    chatbot._faq_repo.buscar_global.return_value = []
    chatbot._claude.gerar_resposta.return_value = RespostaClaude(
        texto="Não tenho certeza, mas...", tokens_entrada=20, tokens_saida=30,
    )
    chatbot._bc_repo.buscar_por_termo.return_value = []
    r = chatbot.responder(estudante, "qual o sentido da vida")
    assert r["tokens"] == 50
    chatbot._claude.gerar_resposta.assert_called_once()


# ---------------------------------------------------------------------------
# Persistência das duas mensagens (pergunta + resposta)
# ---------------------------------------------------------------------------
def test_pergunta_e_resposta_sao_persistidas(chatbot, estudante):
    chatbot._faq_repo.melhor_match.return_value = FaqItem(
        id=1, categoria="login", pergunta="?", resposta="Redefina a senha.", link=None,
    )
    chatbot.responder(estudante, "Esqueci minha senha")
    chamadas = chatbot._conversa_repo.adicionar_mensagem.call_args_list
    assert len(chamadas) == 2
    assert chamadas[0].kwargs["remetente"] == Remetente.USUARIO
    assert chamadas[1].kwargs["remetente"] == Remetente.BOT
