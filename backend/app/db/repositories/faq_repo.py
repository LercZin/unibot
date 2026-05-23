from app.db.connection import pool
from app.domain.faq import FaqItem


def _para_dominio(linha: dict) -> FaqItem:
    return FaqItem(
        id=linha["id"],
        categoria=linha["categoria"],
        pergunta=linha["pergunta"],
        resposta=linha["resposta"],
        link=linha.get("link"),
    )


class FaqRepository:
    """Acesso à tabela `faq_institucional`.

    Estratégia de busca em duas etapas:
    1. Tenta FULLTEXT MATCH (mais relevante por relevância textual).
    2. Cai para LIKE simples se o termo for muito curto para o FULLTEXT
       (mínimo 4 caracteres por padrão no MySQL) ou se nada bateu.
    """

    def listar_por_categoria(self, categoria: str) -> list[FaqItem]:
        with pool.cursor() as cur:
            cur.execute(
                "SELECT * FROM faq_institucional "
                "WHERE categoria = %s AND ativo = 1 ORDER BY id",
                (categoria,),
            )
            return [_para_dominio(r) for r in cur.fetchall()]

    def buscar_global(self, termo: str, limite: int = 3) -> list[FaqItem]:
        """Busca o termo em TODAS as categorias. Usado como fallback quando
        o classificador não conseguiu identificar a intenção."""
        with pool.cursor() as cur:
            cur.execute(
                """
                SELECT *,
                       MATCH(pergunta, resposta, palavras_chave) AGAINST (%s) AS score
                  FROM faq_institucional
                 WHERE ativo = 1
                   AND MATCH(pergunta, resposta, palavras_chave) AGAINST (%s) > 0
                 ORDER BY score DESC
                 LIMIT %s
                """,
                (termo, termo, limite),
            )
            return [_para_dominio({k: v for k, v in r.items() if k != "score"})
                    for r in cur.fetchall()]

    def melhor_match(self, categoria: str, termo: str) -> FaqItem | None:
        """Dentro de uma categoria, escolhe o item mais aderente ao termo do usuário."""
        with pool.cursor() as cur:
            cur.execute(
                """
                SELECT *,
                       MATCH(pergunta, resposta, palavras_chave) AGAINST (%s) AS score
                  FROM faq_institucional
                 WHERE categoria = %s AND ativo = 1
                 ORDER BY score DESC, id
                 LIMIT 1
                """,
                (termo, categoria),
            )
            linha = cur.fetchone()
            if linha and linha.get("score", 0) > 0:
                linha.pop("score", None)
                return _para_dominio(linha)

        # Fallback: pega o primeiro item ativo da categoria
        itens = self.listar_por_categoria(categoria)
        return itens[0] if itens else None
