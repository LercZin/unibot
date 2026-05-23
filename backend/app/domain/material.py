from dataclasses import dataclass
from enum import Enum


class TipoMaterial(str, Enum):
    VIDEO = "video"
    PDF = "pdf"
    ARTIGO = "artigo"
    LINK = "link"
    SLIDE = "slide"


@dataclass
class Material:
    id: int
    disciplina_id: int
    titulo: str
    tipo: TipoMaterial
    url: str
    descricao: str = ""
