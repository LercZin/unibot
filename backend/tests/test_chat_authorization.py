"""Object authorization through HTTP routes and real repository queries.

Authentication is supplied by a test dependency. Repository SQL runs against an
in-memory SQLite adapter; this does not replace MySQL integration testing.
"""
from contextlib import contextmanager
from datetime import datetime
from types import SimpleNamespace
import sqlite3
from unittest.mock import MagicMock

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
import pytest

from app.core.exceptions import NotFoundError, register_exception_handlers
from app.db.repositories import conversa_repo
from app.dependencies import somente_estudante
from app.domain.conversa import Remetente
from app.domain.usuario import Estudante
from app.routers import chat
from app.services.chatbot import Chatbot


class CursorAdapter:
    def __init__(self, connection):
        self.cursor = connection.cursor()

    def execute(self, query, parameters=()):
        return self.cursor.execute(query.replace("%s", "?"), parameters)

    def fetchone(self):
        row = self.cursor.fetchone()
        return dict(row) if row is not None else None

    def fetchall(self):
        return [dict(row) for row in self.cursor.fetchall()]

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    @property
    def rowcount(self):
        return self.cursor.rowcount


@pytest.fixture
def environment(monkeypatch):
    database = sqlite3.connect(":memory:", check_same_thread=False)
    database.row_factory = sqlite3.Row
    database.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE conversa (
            id INTEGER PRIMARY KEY, usuario_id INTEGER NOT NULL, titulo TEXT,
            data_inicio TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE mensagem (
            id INTEGER PRIMARY KEY, conversa_id INTEGER REFERENCES conversa(id),
            remetente TEXT, texto TEXT, intencao TEXT, tokens_usados INTEGER,
            data_envio TEXT DEFAULT CURRENT_TIMESTAMP
        );
        INSERT INTO conversa (id, usuario_id, titulo) VALUES (11, 1, 'Student A'), (22, 2, 'Student B');
        INSERT INTO mensagem (conversa_id, remetente, texto) VALUES
            (11, 'usuario', 'Private A'), (22, 'usuario', 'Private B');
    """)

    @contextmanager
    def cursor():
        adapter = CursorAdapter(database)
        try:
            yield adapter
            database.commit()
        except Exception:
            database.rollback()
            raise
        finally:
            adapter.cursor.close()

    monkeypatch.setattr(conversa_repo, "pool", SimpleNamespace(cursor=cursor))
    repository = conversa_repo.ConversaRepository()
    provider = MagicMock()
    bot = Chatbot(conversa_repo=repository, claude=provider)
    monkeypatch.setattr(chat, "_conv_repo", repository)
    monkeypatch.setattr(chat, "_chatbot", bot)

    def authenticated_student(request: Request):
        student_id = int(request.headers.get("X-Test-Student", "1"))
        return Estudante(
            id=student_id, nome=f"Student {student_id}", email=f"student{student_id}@example.test",
            senha_hash="test-only", data_cadastro=datetime(2026, 1, 1), ativo=True,
            matricula=str(student_id), curso="Demo", semestre=1,
        )

    app = FastAPI()
    app.include_router(chat.router)
    register_exception_handlers(app)
    app.dependency_overrides[somente_estudante] = authenticated_student
    with TestClient(app) as client:
        yield SimpleNamespace(client=client, database=database, repository=repository, provider=provider)
    database.close()


@pytest.mark.parametrize("student_id, own_id, foreign_id", [(1, 11, 22), (2, 22, 11)])
def test_history_rejects_another_students_conversation(environment, student_id, own_id, foreign_id):
    response = environment.client.get(
        f"/api/chat/historico?conversa_id={foreign_id}", headers={"X-Test-Student": str(student_id)},
    )
    assert response.status_code == 404
    assert "Private" not in response.text
    assert environment.client.get(
        f"/api/chat/historico?conversa_id={own_id}", headers={"X-Test-Student": str(student_id)},
    ).status_code == 200


@pytest.mark.parametrize("student_id, foreign_id", [(1, 22), (2, 11)])
def test_message_to_another_students_conversation_has_no_effect(environment, student_id, foreign_id):
    before = environment.database.execute("SELECT COUNT(*) FROM mensagem").fetchone()[0]
    response = environment.client.post(
        "/api/chat/mensagens", json={"texto": "Oi!", "conversa_id": foreign_id},
        headers={"X-Test-Student": str(student_id)},
    )
    assert response.status_code == 404
    assert environment.database.execute("SELECT COUNT(*) FROM mensagem").fetchone()[0] == before
    environment.provider.gerar_resposta.assert_not_called()


def test_own_conversation_can_be_read_and_appended(environment):
    response = environment.client.post("/api/chat/mensagens", json={"texto": "Oi!", "conversa_id": 11})
    assert response.status_code == 200
    assert response.json()["conversa_id"] == 11
    history = environment.client.get("/api/chat/historico?conversa_id=11").json()
    assert [message["remetente"] for message in history] == ["usuario", "usuario", "bot"]
    assert all(message["texto"] != "Private B" for message in history)


def test_missing_and_foreign_conversations_are_indistinguishable(environment):
    missing = environment.client.get("/api/chat/historico?conversa_id=999")
    foreign = environment.client.get("/api/chat/historico?conversa_id=22")
    assert missing.status_code == foreign.status_code == 404
    assert missing.json() == foreign.json()


def test_default_history_uses_only_authenticated_students_conversation(environment):
    response = environment.client.get("/api/chat/historico")
    assert response.status_code == 200
    assert [message["texto"] for message in response.json()] == ["Private A"]


def test_message_without_id_creates_a_conversation_owned_by_the_authenticated_student(environment):
    response = environment.client.post(
        "/api/chat/mensagens", json={"texto": "Oi!"}, headers={"X-Test-Student": "3"},
    )
    assert response.status_code == 200
    conversation_id = response.json()["conversa_id"]
    owner = environment.database.execute(
        "SELECT usuario_id FROM conversa WHERE id=?", (conversation_id,),
    ).fetchone()[0]
    assert owner == 3
    assert len(environment.client.get(
        "/api/chat/historico", headers={"X-Test-Student": "3"},
    ).json()) == 2


def test_message_to_missing_conversation_has_no_effect(environment):
    response = environment.client.post(
        "/api/chat/mensagens", json={"texto": "Oi!", "conversa_id": 999},
    )
    assert response.status_code == 404
    assert environment.database.execute("SELECT COUNT(*) FROM mensagem").fetchone()[0] == 2
    environment.provider.gerar_resposta.assert_not_called()


@pytest.mark.parametrize("conversation_id", [0, -1])
def test_invalid_conversation_identifiers_are_rejected(environment, conversation_id):
    assert environment.client.get(f"/api/chat/historico?conversa_id={conversation_id}").status_code == 422
    assert environment.client.post(
        "/api/chat/mensagens", json={"texto": "Oi!", "conversa_id": conversation_id},
    ).status_code == 422


@pytest.mark.parametrize("limit", [-1, 0, 101])
def test_history_limit_is_bounded(environment, limit):
    assert environment.client.get(f"/api/chat/historico?limite={limit}").status_code == 422


def test_repository_read_cannot_bypass_owner_scope(environment):
    assert environment.repository.listar_mensagens(22, usuario_id=1) == []


def test_repository_write_cannot_bypass_owner_scope(environment):
    with pytest.raises(NotFoundError):
        environment.repository.adicionar_mensagem(
            conversa_id=22, usuario_id=1, remetente=Remetente.USUARIO,
            texto="Must not be stored", intencao=None,
        )
    assert environment.database.execute("SELECT COUNT(*) FROM mensagem WHERE conversa_id=22").fetchone()[0] == 1
