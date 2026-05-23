from dataclasses import dataclass
from datetime import date
from enum import Enum


class StatusMatricula(str, Enum):
    ATIVA = "ativa"
    TRANCADA = "trancada"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


@dataclass
class Matricula:
    id: int
    estudante_id: int
    disciplina_id: int
    periodo: str
    status: StatusMatricula = StatusMatricula.ATIVA
    data_matricula: date | None = None
