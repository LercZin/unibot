from app.db.connection import pool
from app.domain.prazo import Prazo, TipoPrazo


def _para_dominio(linha: dict) -> Prazo:
    return Prazo(
        id=linha["id"],
        disciplina_id=linha["disciplina_id"],
        titulo=linha["titulo"],
        descricao=linha["descricao"] or "",
        tipo=TipoPrazo(linha["tipo"]),
        data_entrega=linha["data_entrega"],
    )


class PrazoRepository:
    def listar_por_disciplina(self, disciplina_id: int) -> list[Prazo]:
        with pool.cursor() as cur:
            cur.execute(
                "SELECT * FROM prazo WHERE disciplina_id = %s ORDER BY data_entrega",
                (disciplina_id,),
            )
            return [_para_dominio(r) for r in cur.fetchall()]

    def listar_proximos_do_estudante(self, estudante_id: int, limite: int = 10) -> list[Prazo]:
        with pool.cursor() as cur:
            cur.execute(
                """
                SELECT p.*
                  FROM prazo p
                  JOIN matricula m ON m.disciplina_id = p.disciplina_id
                 WHERE m.estudante_id = %s
                   AND m.status = 'ativa'
                   AND p.data_entrega >= NOW()
                 ORDER BY p.data_entrega
                 LIMIT %s
                """,
                (estudante_id, limite),
            )
            return [_para_dominio(r) for r in cur.fetchall()]

    def criar(self, *, disciplina_id: int, titulo: str, descricao: str,
              tipo: TipoPrazo, data_entrega) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO prazo (disciplina_id, titulo, descricao, tipo, data_entrega) "
                "VALUES (%s, %s, %s, %s, %s)",
                (disciplina_id, titulo, descricao, tipo.value, data_entrega),
            )
            return cur.lastrowid
