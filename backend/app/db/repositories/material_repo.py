from app.db.connection import pool
from app.domain.material import Material, TipoMaterial


def _para_dominio(linha: dict) -> Material:
    return Material(
        id=linha["id"],
        disciplina_id=linha["disciplina_id"],
        titulo=linha["titulo"],
        tipo=TipoMaterial(linha["tipo"]),
        url=linha["url"],
        descricao=linha["descricao"] or "",
    )


class MaterialRepository:
    def listar_por_disciplina(self, disciplina_id: int) -> list[Material]:
        with pool.cursor() as cur:
            cur.execute(
                "SELECT * FROM material WHERE disciplina_id = %s ORDER BY titulo",
                (disciplina_id,),
            )
            return [_para_dominio(r) for r in cur.fetchall()]

    def criar(self, *, disciplina_id: int, titulo: str, tipo: TipoMaterial,
              url: str, descricao: str) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO material (disciplina_id, titulo, tipo, url, descricao) "
                "VALUES (%s, %s, %s, %s, %s)",
                (disciplina_id, titulo, tipo.value, url, descricao),
            )
            return cur.lastrowid
