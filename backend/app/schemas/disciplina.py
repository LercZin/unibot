from pydantic import BaseModel, Field


class DisciplinaOut(BaseModel):
    id: int
    codigo: str
    nome: str
    carga_horaria: int
    ementa: str
    professor_id: int | None = None


class CriarDisciplinaIn(BaseModel):
    codigo: str = Field(min_length=2, max_length=20)
    nome: str = Field(min_length=2, max_length=120)
    carga_horaria: int = Field(ge=1, le=400)
    ementa: str = ""
    professor_id: int | None = None
