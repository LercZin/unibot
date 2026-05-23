from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.db.connection import pool
from app.routers import (
    admin, aluno, auth, chat, disciplinas, materiais, notas, prazos, usuarios,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    pool.ping()
    yield
    pool.close()


app = FastAPI(
    title="UniBot API",
    description="Assistente acadêmico inteligente — Anhanguera",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(disciplinas.router)
app.include_router(prazos.router)
app.include_router(notas.router)
app.include_router(materiais.router)
app.include_router(chat.router)
app.include_router(aluno.router)
app.include_router(admin.router)


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "service": "unibot-api"}
