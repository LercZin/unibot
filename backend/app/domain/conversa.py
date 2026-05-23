from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Remetente(str, Enum):
    USUARIO = "usuario"
    BOT = "bot"


class IntencaoMensagem(str, Enum):
    SAUDACAO = "saudacao"

    # Acadêmico (acessa dados reais do estudante)
    CONSULTA_NOTA = "consulta_nota"
    CONSULTA_PRAZO = "consulta_prazo"
    PEDIDO_MATERIAL = "pedido_material"

    # Conteúdo didático (vai para Claude com contexto da base de conhecimento)
    DUVIDA_CONTEUDO = "duvida_conteudo"
    GERAR_RESUMO = "gerar_resumo"
    GERAR_QUIZ = "gerar_quiz"

    # FAQ institucional (resposta determinística da tabela faq_institucional)
    FAQ_FINANCEIRO = "faq_financeiro"
    FAQ_HISTORICO = "faq_historico"
    FAQ_DECLARACAO_MATRICULA = "faq_declaracao_matricula"
    FAQ_CALENDARIO = "faq_calendario"
    FAQ_RENOVACAO = "faq_renovacao"
    FAQ_TRANCAMENTO = "faq_trancamento"
    FAQ_LOGIN = "faq_login"
    FAQ_ESTAGIO = "faq_estagio"
    FAQ_TCC = "faq_tcc"
    FAQ_DIPLOMA = "faq_diploma"
    FAQ_SECRETARIA = "faq_secretaria"

    OUTRO = "outro"

    @property
    def categoria_faq(self) -> str | None:
        """Mapeia a intenção para a coluna `categoria` da tabela faq_institucional.
        Retorna None se a intenção não tem FAQ associada."""
        return _INTENCAO_PARA_CATEGORIA.get(self)


_INTENCAO_PARA_CATEGORIA: dict["IntencaoMensagem", str] = {}
# Preenchido depois que o Enum termina de construir-se
def _bind_faq_map() -> None:
    _INTENCAO_PARA_CATEGORIA.update({
        IntencaoMensagem.CONSULTA_NOTA:            "notas",
        IntencaoMensagem.FAQ_FINANCEIRO:           "financeiro",
        IntencaoMensagem.FAQ_HISTORICO:            "historico",
        IntencaoMensagem.FAQ_DECLARACAO_MATRICULA: "declaracao_matricula",
        IntencaoMensagem.FAQ_CALENDARIO:           "calendario",
        IntencaoMensagem.FAQ_RENOVACAO:            "renovacao",
        IntencaoMensagem.FAQ_TRANCAMENTO:          "trancamento",
        IntencaoMensagem.FAQ_LOGIN:                "login",
        IntencaoMensagem.FAQ_ESTAGIO:              "estagio",
        IntencaoMensagem.FAQ_TCC:                  "tcc",
        IntencaoMensagem.FAQ_DIPLOMA:              "diploma",
        IntencaoMensagem.FAQ_SECRETARIA:           "secretaria",
    })
_bind_faq_map()


@dataclass
class Mensagem:
    id: int
    conversa_id: int
    remetente: Remetente
    texto: str
    data_envio: datetime
    intencao: IntencaoMensagem | None = None
    tokens_usados: int = 0


@dataclass
class Conversa:
    id: int
    usuario_id: int
    titulo: str
    data_inicio: datetime
    mensagens: list[Mensagem] = field(default_factory=list)
