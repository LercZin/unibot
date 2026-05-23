from datetime import datetime

from pydantic import BaseModel, Field


class PrazoOut(BaseModel):
    id: int
    disciplina_id: int
    titulo: str
    descricao: str
    tipo: str
    data_entrega: datetime


class CriarPrazoIn(BaseModel):
    disciplina_id: int
    titulo: str = Field(min_length=2, max_length=120)
    descricao: str = ""
    tipo: str
    data_entrega: datetime
