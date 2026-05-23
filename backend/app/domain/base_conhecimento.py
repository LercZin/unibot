from dataclasses import dataclass, field
from typing import Any


@dataclass
class ItemBaseConhecimento:
    id: int
    disciplina_id: int
    topico: str
    conteudo: str
    metadados: dict[str, Any] = field(default_factory=dict)
