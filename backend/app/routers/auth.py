from fastapi import APIRouter

from app.schemas.auth import LoginIn, TokenOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])
_service = AuthService()


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn):
    return _service.login(payload.email, payload.senha, lembrar=payload.lembrar)
