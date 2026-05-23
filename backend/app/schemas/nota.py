from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class NotaOut(BaseModel):
    id: int
    matricula_id: int
    tipo: str
    valor: Decimal
    peso: Decimal
    data: date


class CriarNotaIn(BaseModel):
    matricula_id: int
    tipo: str = Field(min_length=1, max_length=40)
    valor: Decimal = Field(ge=0, le=10)
    peso: Decimal = Field(gt=0, le=10)
    data: date


class DesempenhoOut(BaseModel):
    disciplina_id: int
    disciplina_nome: str
    notas: list[NotaOut]
    media: Decimal
    situacao: str
