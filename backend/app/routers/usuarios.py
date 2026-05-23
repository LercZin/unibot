from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.security import hash_senha
from app.db.repositories.usuario_repo import UsuarioRepository
from app.dependencies import get_usuario_repo, usuario_atual
from app.domain.usuario import Usuario
from app.schemas.auth import UsuarioOut
from app.schemas.usuario import CriarEstudanteIn

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])


@router.post("/estudantes", status_code=status.HTTP_201_CREATED, response_model=UsuarioOut)
def cadastrar_estudante(
    payload: CriarEstudanteIn,
    repo: Annotated[UsuarioRepository, Depends(get_usuario_repo)],
):
    uid = repo.criar_estudante(
        nome=payload.nome,
        email=payload.email,
        senha_hash=hash_senha(payload.senha),
        matricula=payload.matricula,
        curso=payload.curso,
        semestre=payload.semestre,
    )
    return UsuarioOut(id=uid, nome=payload.nome, email=payload.email, tipo="estudante")


@router.get("/eu", response_model=UsuarioOut)
def meu_perfil(usuario: Annotated[Usuario, Depends(usuario_atual)]):
    return UsuarioOut(
        id=usuario.id, nome=usuario.nome, email=usuario.email, tipo=usuario.tipo.value
    )
