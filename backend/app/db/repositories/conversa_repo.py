from app.db.connection import pool
from app.domain.conversa import Conversa, IntencaoMensagem, Mensagem, Remetente


def _msg_para_dominio(linha: dict) -> Mensagem:
    return Mensagem(
        id=linha["id"],
        conversa_id=linha["conversa_id"],
        remetente=Remetente(linha["remetente"]),
        texto=linha["texto"],
        data_envio=linha["data_envio"],
        intencao=IntencaoMensagem(linha["intencao"]) if linha.get("intencao") else None,
        tokens_usados=linha.get("tokens_usados") or 0,
    )


class ConversaRepository:
    def criar(self, usuario_id: int, titulo: str) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO conversa (usuario_id, titulo) VALUES (%s, %s)",
                (usuario_id, titulo),
            )
            return cur.lastrowid

    def buscar_ou_criar_ativa(self, usuario_id: int) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "SELECT id FROM conversa WHERE usuario_id = %s "
                "ORDER BY data_inicio DESC LIMIT 1",
                (usuario_id,),
            )
            linha = cur.fetchone()
            if linha:
                return linha["id"]
        return self.criar(usuario_id, "Conversa")

    def listar_do_usuario(self, usuario_id: int) -> list[Conversa]:
        with pool.cursor() as cur:
            cur.execute(
                "SELECT * FROM conversa WHERE usuario_id = %s ORDER BY data_inicio DESC",
                (usuario_id,),
            )
            return [
                Conversa(
                    id=r["id"],
                    usuario_id=r["usuario_id"],
                    titulo=r["titulo"],
                    data_inicio=r["data_inicio"],
                )
                for r in cur.fetchall()
            ]

    def listar_mensagens(self, conversa_id: int, limite: int = 50) -> list[Mensagem]:
        with pool.cursor() as cur:
            cur.execute(
                "SELECT * FROM mensagem WHERE conversa_id = %s "
                "ORDER BY data_envio DESC LIMIT %s",
                (conversa_id, limite),
            )
            mensagens = [_msg_para_dominio(r) for r in cur.fetchall()]
        return list(reversed(mensagens))

    def adicionar_mensagem(self, *, conversa_id: int, remetente: Remetente,
                           texto: str, intencao: IntencaoMensagem | None,
                           tokens_usados: int = 0) -> int:
        with pool.cursor() as cur:
            cur.execute(
                "INSERT INTO mensagem (conversa_id, remetente, texto, intencao, tokens_usados) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    conversa_id,
                    remetente.value,
                    texto,
                    intencao.value if intencao else None,
                    tokens_usados,
                ),
            )
            return cur.lastrowid
