from decimal import Decimal

from app.db.connection import pool
from app.domain.nota import calcular_media_ponderada, classificar_situacao


class MatriculaRepository:
    """Consultas agregadas usadas para gerar documentos do aluno."""

    def historico_completo(self, estudante_id: int) -> list[dict]:
        """Todas as matrículas do aluno, com média e situação calculadas.

        Inclui matrículas em qualquer status (ativa, trancada, concluída),
        ordenadas pelo período mais recente primeiro.
        """
        with pool.cursor() as cur:
            cur.execute(
                """
                SELECT m.id            AS matricula_id,
                       m.periodo,
                       m.status,
                       m.data_matricula,
                       d.id            AS disciplina_id,
                       d.codigo,
                       d.nome,
                       d.carga_horaria,
                       d.ementa
                  FROM matricula m
                  JOIN disciplina d ON d.id = m.disciplina_id
                 WHERE m.estudante_id = %s
                 ORDER BY m.periodo DESC, d.nome
                """,
                (estudante_id,),
            )
            matriculas = cur.fetchall()

            for m in matriculas:
                cur.execute(
                    "SELECT tipo, valor, peso, data FROM nota "
                    "WHERE matricula_id = %s ORDER BY data",
                    (m["matricula_id"],),
                )
                m["notas"] = cur.fetchall()

        # Calcula média e situação em Python (regra de negócio fora do SQL)
        from app.domain.nota import Nota
        for m in matriculas:
            notas_dominio = [
                Nota(id=0, matricula_id=m["matricula_id"], tipo=n["tipo"],
                     valor=Decimal(str(n["valor"])), peso=Decimal(str(n["peso"])),
                     data=n["data"])
                for n in m["notas"]
            ]
            media = calcular_media_ponderada(notas_dominio)
            m["media"] = media
            m["situacao"] = (
                classificar_situacao(media) if notas_dominio
                else ("em_curso" if m["status"] == "ativa" else m["status"])
            )
        return matriculas

    def matriculas_ativas(self, estudante_id: int, periodo: str | None = None) -> list[dict]:
        sql = """
            SELECT m.id AS matricula_id, m.periodo, m.status,
                   d.id AS disciplina_id, d.codigo, d.nome, d.carga_horaria
              FROM matricula m
              JOIN disciplina d ON d.id = m.disciplina_id
             WHERE m.estudante_id = %s AND m.status = 'ativa'
        """
        params: tuple = (estudante_id,)
        if periodo:
            sql += " AND m.periodo = %s"
            params += (periodo,)
        sql += " ORDER BY d.nome"

        with pool.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
