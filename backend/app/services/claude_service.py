from dataclasses import dataclass

import anthropic
from anthropic import APIError

from app.core.config import settings
from app.core.exceptions import ClaudeAPIError
from app.core.logging import logger


@dataclass
class RespostaClaude:
    texto: str
    tokens_entrada: int
    tokens_saida: int

    @property
    def total_tokens(self) -> int:
        return self.tokens_entrada + self.tokens_saida


class ClaudeService:
    """Wrapper fino sobre o SDK oficial da Anthropic.

    Centraliza a chamada à API para isolar a dependência externa do resto do
    sistema, facilitar testes (basta mockar essa classe) e tratar falhas de
    forma uniforme — em caso de erro, levanta `ClaudeAPIError`, que vira
    HTTP 503 com mensagem amigável (atende ao RNF10).
    """

    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._model = settings.claude_model
        self._max_tokens = settings.claude_max_tokens

    def gerar_resposta(
        self,
        *,
        system_prompt: str,
        historico: list[dict],
        mensagem_usuario: str,
    ) -> RespostaClaude:
        try:
            resposta = self._client.messages.create(
                model=self._model,
                max_tokens=self._max_tokens,
                system=system_prompt,
                messages=[*historico, {"role": "user", "content": mensagem_usuario}],
            )
        except APIError as e:
            logger.exception("Falha na chamada ao Claude")
            raise ClaudeAPIError("Não foi possível falar com o assistente agora. Tente novamente.") from e

        texto = "".join(
            bloco.text for bloco in resposta.content if getattr(bloco, "type", None) == "text"
        )
        return RespostaClaude(
            texto=texto,
            tokens_entrada=resposta.usage.input_tokens,
            tokens_saida=resposta.usage.output_tokens,
        )
