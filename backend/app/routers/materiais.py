from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.db.repositories.material_repo import MaterialRepository
from app.dependencies import somente_professor, usuario_atual
from app.domain.material import TipoMaterial
from app.domain.usuario import Professor, Usuario
from app.schemas.material import CriarMaterialIn, MaterialOut

router = APIRouter(prefix="/api/materiais", tags=["materiais"])
_repo = MaterialRepository()


@router.get("/disciplina/{disciplina_id}", response_model=list[MaterialOut])
def listar_por_disciplina(
    disciplina_id: int,
    _: Annotated[Usuario, Depends(usuario_atual)],
):
    return [
        MaterialOut(**m.__dict__)
        for m in _repo.listar_por_disciplina(disciplina_id)
    ]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=MaterialOut)
def criar(payload: CriarMaterialIn, _: Annotated[Professor, Depends(somente_professor)]):
    mid = _repo.criar(
        disciplina_id=payload.disciplina_id,
        titulo=payload.titulo,
        tipo=TipoMaterial(payload.tipo),
        url=str(payload.url),
        descricao=payload.descricao,
    )
    return MaterialOut(
        id=mid,
        disciplina_id=payload.disciplina_id,
        titulo=payload.titulo,
        tipo=payload.tipo,
        url=str(payload.url),
        descricao=payload.descricao,
    )
