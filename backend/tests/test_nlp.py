import pytest

from app.domain.conversa import IntencaoMensagem
from app.services.processador_nlp import ProcessadorNLP


@pytest.fixture
def nlp():
    return ProcessadorNLP()


@pytest.mark.parametrize("texto,esperado", [
    # Saudação
    ("Olá, tudo bem?",                            IntencaoMensagem.SAUDACAO),

    # Acadêmico real
    ("Como estou em Estatística?",                IntencaoMensagem.CONSULTA_NOTA),
    ("Onde fica meu boletim?",                    IntencaoMensagem.CONSULTA_NOTA),
    ("Fui aprovado ou reprovado?",                IntencaoMensagem.CONSULTA_NOTA),
    ("Quando saem as notas?",                     IntencaoMensagem.CONSULTA_NOTA),
    ("Qual a próxima entrega de POO?",            IntencaoMensagem.CONSULTA_PRAZO),

    # FAQ financeiro
    ("Como emito um boleto?",                     IntencaoMensagem.FAQ_FINANCEIRO),
    ("Preciso da 2ª via da minha mensalidade",    IntencaoMensagem.FAQ_FINANCEIRO),
    ("Quando vence meu pagamento?",               IntencaoMensagem.FAQ_FINANCEIRO),
    ("Estou inadimplente, o que faço?",           IntencaoMensagem.FAQ_FINANCEIRO),

    # FAQ histórico
    ("Como pego meu histórico?",                  IntencaoMensagem.FAQ_HISTORICO),
    ("Preciso do histórico escolar",              IntencaoMensagem.FAQ_HISTORICO),

    # FAQ declaração
    ("Como emito declaração de matrícula?",       IntencaoMensagem.FAQ_DECLARACAO_MATRICULA),
    ("Declaração para o banco",                   IntencaoMensagem.FAQ_DECLARACAO_MATRICULA),

    # FAQ calendário
    ("Quando começam as aulas?",                  IntencaoMensagem.FAQ_CALENDARIO),
    ("Quais são as datas do semestre?",           IntencaoMensagem.FAQ_CALENDARIO),
    ("Quando é o período de provas?",             IntencaoMensagem.FAQ_CALENDARIO),
    ("Quando são as férias?",                     IntencaoMensagem.FAQ_CALENDARIO),

    # FAQ renovação
    ("Como renovo minha matrícula?",              IntencaoMensagem.FAQ_RENOVACAO),
    ("Quero continuar no próximo semestre",       IntencaoMensagem.FAQ_RENOVACAO),

    # FAQ trancamento
    ("Quero trancar minha matrícula",             IntencaoMensagem.FAQ_TRANCAMENTO),
    ("Como pausar meus estudos?",                 IntencaoMensagem.FAQ_TRANCAMENTO),

    # FAQ login
    ("Esqueci minha senha",                       IntencaoMensagem.FAQ_LOGIN),
    ("Não consigo acessar o portal",              IntencaoMensagem.FAQ_LOGIN),
    ("Minha conta está bloqueada",                IntencaoMensagem.FAQ_LOGIN),
    ("Primeiro acesso ao sistema",                IntencaoMensagem.FAQ_LOGIN),

    # FAQ estágio
    ("Como faço para estagiar?",                  IntencaoMensagem.FAQ_ESTAGIO),
    ("Quais vagas de estágio existem?",           IntencaoMensagem.FAQ_ESTAGIO),

    # FAQ TCC
    ("Preciso de informações sobre o TCC",        IntencaoMensagem.FAQ_TCC),
    ("Como escolho meu orientador?",              IntencaoMensagem.FAQ_TCC),
    ("Normas da monografia",                      IntencaoMensagem.FAQ_TCC),

    # FAQ diploma
    ("Como solicito meu diploma?",                IntencaoMensagem.FAQ_DIPLOMA),
    ("Quando é a colação de grau?",               IntencaoMensagem.FAQ_DIPLOMA),

    # FAQ secretaria
    ("Quero falar com uma pessoa",                IntencaoMensagem.FAQ_SECRETARIA),
    ("Telefone da secretaria",                    IntencaoMensagem.FAQ_SECRETARIA),
    ("Atendimento presencial",                    IntencaoMensagem.FAQ_SECRETARIA),

    # Conteúdo didático
    ("Explica o que é polimorfismo",              IntencaoMensagem.DUVIDA_CONTEUDO),
    ("Pode fazer um resumo do conteúdo?",         IntencaoMensagem.GERAR_RESUMO),
    ("Manda um quiz pra eu praticar",             IntencaoMensagem.GERAR_QUIZ),

    # Catch-all
    ("Bla bla bla nada haver",                    IntencaoMensagem.OUTRO),
])
def test_identificar_intencao(nlp, texto, esperado):
    assert nlp.identificar_intencao(texto) == esperado


def test_extrair_disciplina_mencionada(nlp):
    assert nlp.extrair_disciplina_mencionada(
        "Tenho dúvida em Estatística", ["Cálculo", "Estatística"]
    ) == "Estatística"


def test_categoria_faq_mapping():
    assert IntencaoMensagem.FAQ_FINANCEIRO.categoria_faq == "financeiro"
    assert IntencaoMensagem.FAQ_DIPLOMA.categoria_faq == "diploma"
    assert IntencaoMensagem.DUVIDA_CONTEUDO.categoria_faq is None
