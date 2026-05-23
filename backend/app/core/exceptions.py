from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UniBotError(Exception):
    status_code: int = 400

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class NotFoundError(UniBotError):
    status_code = 404


class UnauthorizedError(UniBotError):
    status_code = 401


class ForbiddenError(UniBotError):
    status_code = 403


class ConflictError(UniBotError):
    status_code = 409


class ClaudeAPIError(UniBotError):
    status_code = 503


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UniBotError)
    async def _handler(_: Request, exc: UniBotError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"erro": exc.__class__.__name__, "mensagem": exc.mensagem},
        )
