from app.db.connection import pool
from app.domain.usuario import TipoUsuario, Usuario, construir_usuario

_SELECT_BASE = """
    SELECT u.id, u.nome, u.email, u.senha_hash, u.tipo, u.data_cadastro, u.ativo,
           e.matricula, e.curso, e.semestre,
           p.registro_docente, p.titulacao,
           a.departamento
      FROM usuario u
 LEFT JOIN estudante       e ON e.usuario_id = u.id
 LEFT JOIN professor       p ON p.usuario_id = u.id
 LEFT JOIN administrador   a ON a.usuario_id = u.id
"""


class UsuarioRepository:
    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        with pool.cursor() as cur:
            cur.execute(_SELECT_BASE + " WHERE u.id = %s", (usuario_id,))
            linha = cur.fetchone()
        return construir_usuario(linha) if linha else None

    def buscar_por_email(self, email: str) -> Usuario | None:
        with pool.cursor() as cur:
            cur.execute(_SELECT_BASE + " WHERE u.email = %s", (email,))
            linha = cur.fetchone()
        return construir_usuario(linha) if linha else None

    def listar(self, tipo: TipoUsuario | None = None) -> list[Usuario]:
        sql = _SELECT_BASE
        params: tuple = ()
        if tipo is not None:
            sql += " WHERE u.tipo = %s"
            params = (tipo.value,)
        sql += " ORDER BY u.nome"
        with pool.cursor() as cur:
            cur.execute(sql, params)
            return [construir_usuario(r) for r in cur.fetchall()]

    def criar_estudante(self, *, nome: str, email: str, senha_hash: str,
                        matricula: str, curso: str, semestre: int) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO usuario (nome, email, senha_hash, tipo) "
                "VALUES (%s, %s, %s, 'estudante')",
                (nome, email, senha_hash),
            )
            uid = cur.lastrowid
            cur.execute(
                "INSERT INTO estudante (usuario_id, matricula, curso, semestre) "
                "VALUES (%s, %s, %s, %s)",
                (uid, matricula, curso, semestre),
            )
        return uid

    def criar_professor(self, *, nome: str, email: str, senha_hash: str,
                        registro_docente: str, titulacao: str) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO usuario (nome, email, senha_hash, tipo) "
                "VALUES (%s, %s, %s, 'professor')",
                (nome, email, senha_hash),
            )
            uid = cur.lastrowid
            cur.execute(
                "INSERT INTO professor (usuario_id, registro_docente, titulacao) "
                "VALUES (%s, %s, %s)",
                (uid, registro_docente, titulacao),
            )
        return uid

    def definir_ativo(self, usuario_id: int, ativo: bool) -> None:
        with pool.cursor() as cur:
            cur.execute("UPDATE usuario SET ativo = %s WHERE id = %s", (ativo, usuario_id))
