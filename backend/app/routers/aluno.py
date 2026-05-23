"""Endpoints que entregam documentos do aluno usando dados reais do banco.

Cada endpoint devolve um JSON que o frontend renderiza como um documento
oficial (com botão de imprimir / salvar em PDF).
"""
from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from app.db.repositories.matricula_repo import MatriculaRepository
from app.dependencies import somente_estudante
from app.domain.usuario import Estudante

router = APIRouter(prefix="/api/aluno", tags=["aluno"])
_repo = MatriculaRepository()


def _periodo_atual() -> str:
    """Retorna o período letivo atual no formato YYYY.{1|2}."""
    hoje = date.today()
    return f"{hoje.year}.{1 if hoje.month <= 6 else 2}"


def _identidade(estudante: Estudante) -> dict:
    return {
        "id":        estudante.id,
        "nome":      estudante.nome,
        "matricula": estudante.matricula,
        "curso":     estudante.curso,
        "semestre":  estudante.semestre,
        "email":     estudante.email,
    }


@router.get("/historico")
def historico_escolar(estudante: Annotated[Estudante, Depends(somente_estudante)]):
    """Histórico escolar completo — todas as disciplinas, notas e situação."""
    matriculas = _repo.historico_completo(estudante.id)

    total_ch = sum(m["carga_horaria"] for m in matriculas
                   if m["situacao"] == "aprovado")
    return {
        "aluno":             _identidade(estudante),
        "emitido_em":        datetime.now().isoformat(timespec="seconds"),
        "codigo_verificacao": f"UB-{estudante.id:04d}-{datetime.now():%Y%m%d}",
        "total_disciplinas": len(matriculas),
        "total_aprovadas":   sum(1 for m in matriculas if m["situacao"] == "aprovado"),
        "carga_horaria_aprovada": total_ch,
        "matriculas": [
            {
                "periodo":       m["periodo"],
                "status":        m["status"],
                "disciplina_id": m["disciplina_id"],
                "codigo":        m["codigo"],
                "nome":          m["nome"],
                "carga_horaria": m["carga_horaria"],
                "media":         str(m["media"]),
                "situacao":      m["situacao"],
                "notas": [
                    {"tipo": n["tipo"], "valor": str(n["valor"]),
                     "peso": str(n["peso"]),
                     "data": n["data"].isoformat() if n["data"] else None}
                    for n in m["notas"]
                ],
            }
            for m in matriculas
        ],
    }


@router.get("/atestado")
def atestado_matricula(estudante: Annotated[Estudante, Depends(somente_estudante)]):
    """Atestado/Declaração de matrícula do período letivo atual."""
    periodo = _periodo_atual()
    matriculas = _repo.matriculas_ativas(estudante.id, periodo=periodo)

    return {
        "aluno":           _identidade(estudante),
        "periodo_letivo":  periodo,
        "emitido_em":      datetime.now().isoformat(timespec="seconds"),
        "validade_dias":   60,
        "codigo_verificacao": f"AT-{estudante.id:04d}-{datetime.now():%Y%m%d%H%M}",
        "disciplinas_matriculadas": [
            {
                "codigo": m["codigo"],
                "nome": m["nome"],
                "carga_horaria": m["carga_horaria"],
            }
            for m in matriculas
        ],
    }


@router.get("/carteirinha")
def carteirinha_digital(estudante: Annotated[Estudante, Depends(somente_estudante)]):
    """Dados para renderizar a carteirinha digital do estudante."""
    return {
        "aluno":      _identidade(estudante),
        "validade":   f"{date.today().year + 1}-12-31",
        "qr_codigo":  f"UNIBOT:{estudante.matricula}:{date.today():%Y%m%d}",
    }
