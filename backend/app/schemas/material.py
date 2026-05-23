from pydantic import BaseModel, Field, HttpUrl


class MaterialOut(BaseModel):
    id: int
    disciplina_id: int
    titulo: str
    tipo: str
    url: str
    descricao: str


class CriarMaterialIn(BaseModel):
    disciplina_id: int
    titulo: str = Field(min_length=2, max_length=120)
    tipo: str
    url: HttpUrl
    descricao: str = ""
