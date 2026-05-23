import re
import unicodedata

from app.domain.conversa import IntencaoMensagem


def _normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


# A ordem importa: padrões mais específicos antes dos genéricos.
# Ex.: "boleto" (financeiro) tem que vir antes que algo que case com "como".
_PADROES: list[tuple[IntencaoMensagem, list[str]]] = [
    # ------ Saudação ------
    (IntencaoMensagem.SAUDACAO, [
        r"\b(oi|ola|bom dia|boa tarde|boa noite|e ai|salve)\b",
    ]),

    # ------ FAQ Financeiro ------
    (IntencaoMensagem.FAQ_FINANCEIRO, [
        r"\bboleto[s]?\b", r"\bmensalidade[s]?\b", r"\bfinanceiro\b",
        r"\bvencimento\b", r"\binadimplen(te|cia)\b", r"\bpagamento\b",
        r"\b2[a\.]? via\b", r"\bsegunda via\b",
    ]),

    # ------ FAQ Histórico ------
    (IntencaoMensagem.FAQ_HISTORICO, [
        r"\bhistorico( escolar)?\b", r"\bdisciplinas cursadas\b",
        r"\bdocumento .* disciplinas\b",
    ]),

    # ------ FAQ Declaração de matrícula ------
    (IntencaoMensagem.FAQ_DECLARACAO_MATRICULA, [
        r"\bdeclaracao (de )?matricula\b", r"\bcomprovante .* matricul",
        r"\bdeclaracao (pa)?ra (o )?(banco|inss|trabalho|plano)\b",
    ]),

    # ------ FAQ Calendário ------
    (IntencaoMensagem.FAQ_CALENDARIO, [
        r"\bcalendario( academico)?\b",
        r"\bcomec[ao]m? as aulas\b", r"\binicio das aulas\b",
        r"\bdatas do semestre\b", r"\bperiodo de provas\b",
        r"\b(quando|datas?) .* ferias\b", r"\brecesso\b",
    ]),

    # ------ FAQ Renovação ------
    (IntencaoMensagem.FAQ_RENOVACAO, [
        r"\breno(?:var|vo|va|vacao) .*matricula\b", r"\brematricula\b",
        r"\bcontinuar no proximo semestre\b", r"\bperiodo de rematricula\b",
    ]),

    # ------ FAQ Trancamento ------
    (IntencaoMensagem.FAQ_TRANCAMENTO, [
        r"\btrancar (a |minha )?matricula\b", r"\btrancamento\b",
        r"\bpausar .* estudos\b", r"\bafastar (-me )?por um semestre\b",
    ]),

    # ------ FAQ Login ------
    (IntencaoMensagem.FAQ_LOGIN, [
        r"\besqueci .* senha\b", r"\bredefinir senha\b",
        r"\bnao consigo (acessar|entrar)\b",
        r"\bconta .* bloquead(?:a|o)\b", r"\bbloqueada\b",
        r"\bprimeiro acesso\b",
    ]),

    # ------ FAQ Estágio ------
    (IntencaoMensagem.FAQ_ESTAGIO, [
        r"\bestagi(o|ar|aria)\b", r"\bcontrato de estagio\b",
        r"\b(vaga[s]? de )?estagio\b", r"\btermo de compromisso\b",
    ]),

    # ------ FAQ TCC ------
    (IntencaoMensagem.FAQ_TCC, [
        r"\btcc\b", r"\bmonografia\b", r"\borientador\b",
        r"\btrabalho de conclusao\b",
    ]),

    # ------ FAQ Diploma / Formatura ------
    (IntencaoMensagem.FAQ_DIPLOMA, [
        r"\bdiploma\b", r"\bcolacao( de grau)?\b", r"\bformatura\b",
        r"\bcertificado de conclusao\b",
    ]),

    # ------ FAQ Secretaria / atendimento humano ------
    (IntencaoMensagem.FAQ_SECRETARIA, [
        r"\bfalar com (uma |um )?(pessoa|atendente|humano)\b",
        r"\btelefone (da )?secretaria\b", r"\batendimento (presencial|humano)\b",
        r"\be[ -]?mail (de contato|da secretaria)\b",
        r"\bsecretaria\b",
    ]),

    # ------ Acadêmico real (dados do estudante) ------
    (IntencaoMensagem.CONSULTA_NOTA, [
        r"\bnota[s]?\b", r"\bboletim\b", r"\bmedia\b", r"\bdesempenho\b",
        r"\bfui aprovado\b", r"\baprovado ou reprovado\b",
        r"\b(quando )?sai(ram)? as notas\b",
        r"\bcomo (estou|vou)\b",
    ]),
    (IntencaoMensagem.CONSULTA_PRAZO, [
        r"\bprazo[s]?\b", r"\bentrega[s]?\b", r"\bprova[s]?\b",
        r"\bdata de entrega\b", r"\bcronograma\b",
        r"\bproxim[ao] (entrega|prova)\b",
    ]),
    (IntencaoMensagem.PEDIDO_MATERIAL, [
        r"\bmaterial[is]?\b", r"\bvideo[s]?\b", r"\bpdf\b",
        r"\bapostila\b", r"\blink[s]? (do|de) (estudo|aula)\b",
    ]),

    # ------ Conteúdo didático ------
    (IntencaoMensagem.GERAR_RESUMO, [r"\bresumo\b", r"\bresuma\b", r"\bresumir\b"]),
    (IntencaoMensagem.GERAR_QUIZ,   [r"\bquiz\b", r"\bquestionario\b", r"\bme teste\b"]),
    (IntencaoMensagem.DUVIDA_CONTEUDO, [
        r"\bexpli(que|ca|car)\b", r"\bo que e\b", r"\bcomo funciona\b",
        r"\bdiferen[cç]a entre\b", r"\bexemplo\b", r"\bduvida\b",
    ]),
]


class ProcessadorNLP:
    """Classificador de intenção baseado em regras (RF04).

    Estratégia híbrida do UniBot: para fluxos previsíveis e administrativos
    (financeiro, documentos, calendário, etc.) o classificador identifica
    a categoria e o `Chatbot` responde direto pela FAQ — sem chamar LLM.
    Para conteúdo didático e perguntas abertas, a intenção `DUVIDA_CONTEUDO`
    ou `OUTRO` direciona para o Claude com o contexto adequado.
    """

    def identificar_intencao(self, texto: str) -> IntencaoMensagem:
        norm = _normalizar(texto)
        for intencao, padroes in _PADROES:
            for padrao in padroes:
                if re.search(padrao, norm):
                    return intencao
        return IntencaoMensagem.OUTRO

    def extrair_disciplina_mencionada(self, texto: str, disciplinas: list[str]) -> str | None:
        norm = _normalizar(texto)
        for nome in disciplinas:
            if _normalizar(nome) in norm:
                return nome
        return None
