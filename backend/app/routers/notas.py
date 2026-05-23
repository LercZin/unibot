from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.exceptions import NotFoundError
from app.db.repositories.disciplina_repo import DisciplinaRepository
from app.db.repositories.nota_repo import NotaRepository
from app.dependencies import somente_estudante, somente_professor
from app.domain.nota import calcular_media_ponderada, classificar_situacao
from app.domain.usuario import Estudante, Professor
from app.schemas.nota import CriarNotaIn, DesempenhoOut, NotaOut

router = APIRouter(prefix="/api/notas", tags=["notas"])
_repo = NotaRepository()
_disc_repo = DisciplinaRepository()


@router.get("/desempenho/{disciplina_id}", response_model=DesempenhoOut)
def desempenho(
    disciplina_id: int,
    estudante: Annotated[Estudante, Depends(somente_estudante)],
):
    disciplina = _disc_repo.buscar(disciplina_id)
    if disciplina is None:
        raise NotFoundError("Disciplina não encontrada")
    notas = _repo.listar_do_estudante_em_disciplina(estudante.id, disciplina_id)
    media = calcular_media_ponderada(notas)
    return DesempenhoOut(
        disciplina_id=disciplina.id,
        disciplina_nome=disciplina.nome,
        notas=[NotaOut(**n.__dict__) for n in notas],
        media=media,
        situacao=classificar_situacao(media),
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=NotaOut)
def lancar_nota(payload: CriarNotaIn, _: Annotated[Professor, Depends(somente_professor)]):
    nid = _repo.criar(**payload.model_dump())
    return NotaOut(id=nid, **payload.model_dump())
