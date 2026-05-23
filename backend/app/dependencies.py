from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decodificar_token
from app.db.repositories.usuario_repo import UsuarioRepository
from app.domain.usuario import Administrador, Estudante, Professor, Usuario

bearer = HTTPBearer(auto_error=False)


def get_usuario_repo() -> UsuarioRepository:
    return UsuarioRepository()


def usuario_atual(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    repo: Annotated[UsuarioRepository, Depends(get_usuario_repo)],
) -> Usuario:
    if creds is None:
        raise UnauthorizedError("Token ausente")
    payload = decodificar_token(creds.credentials)
    usuario = repo.buscar_por_id(int(payload["sub"]))
    if usuario is None or not usuario.ativo:
        raise UnauthorizedError("Usuário inválido")
    return usuario


def somente_estudante(usuario: Annotated[Usuario, Depends(usuario_atual)]) -> Estudante:
    if not isinstance(usuario, Estudante):
        raise ForbiddenError("Rota exclusiva para estudantes")
    return usuario


def somente_professor(usuario: Annotated[Usuario, Depends(usuario_atual)]) -> Professor:
    if not isinstance(usuario, Professor):
        raise ForbiddenError("Rota exclusiva para professores")
    return usuario


def somente_admin(usuario: Annotated[Usuario, Depends(usuario_atual)]) -> Administrador:
    if not isinstance(usuario, Administrador):
        raise ForbiddenError("Rota exclusiva para administradores")
    return usuario
