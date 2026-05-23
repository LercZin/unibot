from app.core.config import settings
from app.core.exceptions import UnauthorizedError
from app.core.security import gerar_token, verificar_senha
from app.db.repositories.usuario_repo import UsuarioRepository


class AuthService:
    def __init__(self, repo: UsuarioRepository | None = None) -> None:
        self._repo = repo or UsuarioRepository()

    def login(self, email: str, senha: str, lembrar: bool = False) -> dict:
        usuario = self._repo.buscar_por_email(email)
        if usuario is None or not usuario.ativo:
            raise UnauthorizedError("Credenciais inválidas")
        if not verificar_senha(senha, usuario.senha_hash):
            raise UnauthorizedError("Credenciais inválidas")

        duracao = settings.jwt_expires_min_lembrar if lembrar else settings.jwt_expires_min
        token = gerar_token(usuario.id, usuario.tipo.value, duracao_min=duracao)
        return {
            "access_token": token,
            "token_type": "bearer",
            "expira_em_min": duracao,
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "tipo": usuario.tipo.value,
            },
        }
