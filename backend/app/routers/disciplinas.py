from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.db.repositories.disciplina_repo import DisciplinaRepository
from app.dependencies import somente_estudante, somente_professor
from app.domain.usuario import Estudante, Professor
from app.schemas.disciplina import CriarDisciplinaIn, DisciplinaOut

router = APIRouter(prefix="/api/disciplinas", tags=["disciplinas"])
_repo = DisciplinaRepository()


@router.get("", response_model=list[DisciplinaOut])
def listar():
    return [DisciplinaOut(**d.__dict__) for d in _repo.listar()]


@router.get("/minhas", response_model=list[DisciplinaOut])
def minhas_disciplinas(estudante: Annotated[Estudante, Depends(somente_estudante)]):
    return [DisciplinaOut(**d.__dict__) for d in _repo.listar_do_estudante(estudante.id)]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DisciplinaOut)
def criar(
    payload: CriarDisciplinaIn,
    professor: Annotated[Professor, Depends(somente_professor)],
):
    did = _repo.criar(
        codigo=payload.codigo,
        nome=payload.nome,
        carga_horaria=payload.carga_horaria,
        ementa=payload.ementa,
        professor_id=payload.professor_id or professor.id,
    )
    return DisciplinaOut(id=did, **payload.model_dump(exclude={"professor_id"}),
                         professor_id=payload.professor_id or professor.id)
