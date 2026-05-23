from pydantic import BaseModel, EmailStr, Field


class LoginIn(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=4, max_length=128)
    lembrar: bool = False


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expira_em_min: int
    usuario: UsuarioOut
