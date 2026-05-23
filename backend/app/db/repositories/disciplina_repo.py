from app.db.connection import pool
from app.domain.disciplina import Disciplina


def _para_dominio(linha: dict) -> Disciplina:
    return Disciplina(
        id=linha["id"],
        codigo=linha["codigo"],
        nome=linha["nome"],
        carga_horaria=linha["carga_horaria"],
        ementa=linha["ementa"] or "",
        professor_id=linha.get("professor_id"),
    )


class DisciplinaRepository:
    def listar(self) -> list[Disciplina]:
        with pool.cursor() as cur:
            cur.execute("SELECT * FROM disciplina ORDER BY nome")
            return [_para_dominio(r) for r in cur.fetchall()]

    def listar_do_estudante(self, estudante_id: int) -> list[Disciplina]:
        with pool.cursor() as cur:
            cur.execute(
                """
                SELECT d.*
                  FROM disciplina d
                  JOIN matricula m ON m.disciplina_id = d.id
                 WHERE m.estudante_id = %s AND m.status = 'ativa'
                 ORDER BY d.nome
                """,
                (estudante_id,),
            )
            return [_para_dominio(r) for r in cur.fetchall()]

    def buscar(self, disciplina_id: int) -> Disciplina | None:
        with pool.cursor() as cur:
            cur.execute("SELECT * FROM disciplina WHERE id = %s", (disciplina_id,))
            linha = cur.fetchone()
        return _para_dominio(linha) if linha else None

    def criar(self, *, codigo: str, nome: str, carga_horaria: int,
              ementa: str, professor_id: int | None) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO disciplina (codigo, nome, carga_horaria, ementa, professor_id) "
                "VALUES (%s, %s, %s, %s, %s)",
                (codigo, nome, carga_horaria, ementa, professor_id),
            )
            return cur.lastrowid
