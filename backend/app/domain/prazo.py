from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TipoPrazo(str, Enum):
    PROVA = "prova"
    TRABALHO = "trabalho"
    ATIVIDADE = "atividade"
    PROJETO = "projeto"


@dataclass
class Prazo:
    id: int
    disciplina_id: int
    titulo: str
    descricao: str
    tipo: TipoPrazo
    data_entrega: datetime

    def esta_atrasado(self, referencia: datetime | None = None) -> bool:
        return (referencia or datetime.now()) > self.data_entrega
