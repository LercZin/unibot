import json

from app.db.connection import pool
from app.domain.base_conhecimento import ItemBaseConhecimento


def _para_dominio(linha: dict) -> ItemBaseConhecimento:
    meta = linha.get("metadados")
    if isinstance(meta, str):
        meta = json.loads(meta)
    return ItemBaseConhecimento(
        id=linha["id"],
        disciplina_id=linha["disciplina_id"],
        topico=linha["topico"],
        conteudo=linha["conteudo"],
        metadados=meta or {},
    )


class BaseConhecimentoRepository:
    def buscar_por_disciplina(self, disciplina_id: int) -> list[ItemBaseConhecimento]:
        with pool.cursor() as cur:
            cur.execute(
                "SELECT * FROM base_conhecimento WHERE disciplina_id = %s",
                (disciplina_id,),
            )
            return [_para_dominio(r) for r in cur.fetchall()]

    def buscar_por_termo(self, disciplina_id: int, termo: str, limite: int = 5) -> list[ItemBaseConhecimento]:
        """Busca simples LIKE. Em versões futuras, trocar por FULLTEXT ou embeddings."""
        with pool.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM base_conhecimento
                 WHERE disciplina_id = %s
                   AND (topico LIKE %s OR conteudo LIKE %s)
                 LIMIT %s
                """,
                (disciplina_id, f"%{termo}%", f"%{termo}%", limite),
            )
            return [_para_dominio(r) for r in cur.fetchall()]

    def criar(self, *, disciplina_id: int, topico: str, conteudo: str,
              metadados: dict | None = None) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO base_conhecimento (disciplina_id, topico, conteudo, metadados) "
                "VALUES (%s, %s, %s, %s)",
                (disciplina_id, topico, conteudo, json.dumps(metadados or {})),
            )
            return cur.lastrowid
