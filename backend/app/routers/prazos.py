from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.db.repositories.prazo_repo import PrazoRepository
from app.dependencies import somente_estudante, somente_professor
from app.domain.prazo import TipoPrazo
from app.domain.usuario import Estudante, Professor
from app.schemas.prazo import CriarPrazoIn, PrazoOut

router = APIRouter(prefix="/api/prazos", tags=["prazos"])
_repo = PrazoRepository()


@router.get("/proximos", response_model=list[PrazoOut])
def proximos_do_estudante(estudante: Annotated[Estudante, Depends(somente_estudante)]):
    return [PrazoOut(**p.__dict__) for p in
            _repo.listar_proximos_do_estudante(estudante.id)]


@router.get("/disciplina/{disciplina_id}", response_model=list[PrazoOut])
def por_disciplina(disciplina_id: int):
    return [PrazoOut(**p.__dict__) for p in
            _repo.listar_por_disciplina(disciplina_id)]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PrazoOut)
def criar(payload: CriarPrazoIn, _: Annotated[Professor, Depends(somente_professor)]):
    pid = _repo.criar(
        disciplina_id=payload.disciplina_id,
        titulo=payload.titulo,
        descricao=payload.descricao,
        tipo=TipoPrazo(payload.tipo),
        data_entrega=payload.data_entrega,
    )
    return PrazoOut(id=pid, **payload.model_dump())
