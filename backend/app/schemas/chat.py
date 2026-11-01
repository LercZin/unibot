from datetime import datetime

from pydantic import BaseModel, Field


class MensagemIn(BaseModel):
    texto: str = Field(min_length=1, max_length=2000)
    conversa_id: int | None = Field(default=None, gt=0)


class MensagemOut(BaseModel):
    conversa_id: int
    intencao: str
    resposta: str
    tokens: int


class HistoricoItem(BaseModel):
    id: int
    remetente: str
    texto: str
    data_envio: datetime
    intencao: str | None = None
