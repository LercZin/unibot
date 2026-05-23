from decimal import Decimal

from app.db.connection import pool
from app.domain.nota import Nota


def _para_dominio(linha: dict) -> Nota:
    return Nota(
        id=linha["id"],
        matricula_id=linha["matricula_id"],
        tipo=linha["tipo"],
        valor=Decimal(str(linha["valor"])),
        peso=Decimal(str(linha["peso"])),
        data=linha["data"],
    )


class NotaRepository:
    def listar_do_estudante_em_disciplina(self, estudante_id: int, disciplina_id: int) -> list[Nota]:
        with pool.cursor() as cur:
            cur.execute(
                """
                SELECT n.*
                  FROM nota n
                  JOIN matricula m ON m.id = n.matricula_id
                 WHERE m.estudante_id = %s AND m.disciplina_id = %s
                 ORDER BY n.data
                """,
                (estudante_id, disciplina_id),
            )
            return [_para_dominio(r) for r in cur.fetchall()]

    def criar(self, *, matricula_id: int, tipo: str, valor: Decimal,
              peso: Decimal, data) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO nota (matricula_id, tipo, valor, peso, data) "
                "VALUES (%s, %s, %s, %s, %s)",
                (matricula_id, tipo, valor, peso, data),
            )
            return cur.lastrowid
