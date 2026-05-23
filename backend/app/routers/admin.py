from typing import Annotated

from fastapi import APIRouter, Depends

from app.db.connection import pool
from app.db.repositories.base_conhecimento_repo import BaseConhecimentoRepository
from app.db.repositories.usuario_repo import UsuarioRepository
from app.dependencies import somente_admin, somente_professor
from app.domain.usuario import Administrador, Professor, TipoUsuario
from app.schemas.usuario import UsuarioResumo

router = APIRouter(prefix="/api/admin", tags=["admin"])
_user_repo = UsuarioRepository()
_bc_repo = BaseConhecimentoRepository()


@router.get("/usuarios", response_model=list[UsuarioResumo])
def listar_usuarios(
    _: Annotated[Administrador, Depends(somente_admin)],
    tipo: TipoUsuario | None = None,
):
    return [
        UsuarioResumo(id=u.id, nome=u.nome, email=u.email, tipo=u.tipo.value, ativo=u.ativo)
        for u in _user_repo.listar(tipo)
    ]


@router.patch("/usuarios/{usuario_id}/ativo")
def alterar_status(
    usuario_id: int,
    ativo: bool,
    _: Annotated[Administrador, Depends(somente_admin)],
):
    _user_repo.definir_ativo(usuario_id, ativo)
    return {"ok": True}


@router.get("/relatorios/duvidas-frequentes")
def duvidas_frequentes(_: Annotated[Professor, Depends(somente_professor)]):
    """RF12 — agrupa mensagens por intenção para identificar pontos de atenção."""
    with pool.cursor() as cur:
        cur.execute(
            """
            SELECT intencao, COUNT(*) AS total
              FROM mensagem
             WHERE remetente = 'usuario' AND intencao IS NOT NULL
             GROUP BY intencao
             ORDER BY total DESC
            """
        )
        return cur.fetchall()


@router.post("/base-conhecimento")
def adicionar_base_conhecimento(
    disciplina_id: int,
    topico: str,
    conteudo: str,
    _: Annotated[Administrador, Depends(somente_admin)],
):
    bid = _bc_repo.criar(disciplina_id=disciplina_id, topico=topico, conteudo=conteudo)
    return {"id": bid}
