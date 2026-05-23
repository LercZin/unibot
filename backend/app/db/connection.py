from contextlib import contextmanager
from typing import Iterator

from mysql.connector import pooling
from mysql.connector.pooling import PooledMySQLConnection

from app.core.config import settings
from app.core.logging import logger


class _Pool:
    """Pool de conexões MySQL singleton.

    Encapsula `mysql.connector.pooling.MySQLConnectionPool` e expõe um context
    manager `cursor()` que abre cursor dict, dá commit no sucesso e rollback
    no erro, e devolve a conexão pro pool no `finally`.
    """

    def __init__(self) -> None:
        self._pool: pooling.MySQLConnectionPool | None = None

    def _ensure(self) -> pooling.MySQLConnectionPool:
        if self._pool is None:
            logger.info("Inicializando pool MySQL em %s:%s/%s",
                        settings.db_host, settings.db_port, settings.db_name)
            self._pool = pooling.MySQLConnectionPool(
                pool_name="unibot_pool",
                pool_size=10,
                pool_reset_session=True,
                host=settings.db_host,
                port=settings.db_port,
                user=settings.db_user,
                password=settings.db_password,
                database=settings.db_name,
                charset="utf8mb4",
                use_pure=True,
                autocommit=False,
            )
        return self._pool

    def ping(self) -> None:
        conn = self._ensure().get_connection()
        try:
            conn.ping(reconnect=True, attempts=2, delay=1)
        finally:
            conn.close()

    def close(self) -> None:
        self._pool = None

    @contextmanager
    def connection(self) -> Iterator[PooledMySQLConnection]:
        conn = self._ensure().get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @contextmanager
    def cursor(self, dictionary: bool = True) -> Iterator:
        with self.connection() as conn:
            cur = conn.cursor(dictionary=dictionary)
            try:
                yield cur
            finally:
                cur.close()


pool = _Pool()
