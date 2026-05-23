from dataclasses import dataclass


@dataclass
class Disciplina:
    id: int
    codigo: str
    nome: str
    carga_horaria: int
    ementa: str
    professor_id: int | None = None
