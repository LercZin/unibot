from pydantic import BaseModel, EmailStr, Field


class CriarEstudanteIn(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=128)
    matricula: str = Field(min_length=4, max_length=20)
    curso: str = Field(min_length=2, max_length=80)
    semestre: int = Field(ge=1, le=20)


class CriarProfessorIn(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=128)
    registro_docente: str
    titulacao: str


class UsuarioResumo(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: str
    ativo: bool
