from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.db.repositories.conversa_repo import ConversaRepository
from app.dependencies import somente_estudante
from app.domain.usuario import Estudante
from app.schemas.chat import HistoricoItem, MensagemIn, MensagemOut
from app.services.chatbot import Chatbot

router = APIRouter(prefix="/api/chat", tags=["chat"])
_chatbot = Chatbot()
_conv_repo = ConversaRepository()


@router.post("/mensagens", response_model=MensagemOut)
def enviar_mensagem(
    payload: MensagemIn,
    estudante: Annotated[Estudante, Depends(somente_estudante)],
):
    return _chatbot.responder(estudante, payload.texto, payload.conversa_id)


@router.get("/historico", response_model=list[HistoricoItem])
def historico(
    estudante: Annotated[Estudante, Depends(somente_estudante)],
    conversa_id: Annotated[int | None, Query(gt=0)] = None,
    limite: Annotated[int, Query(ge=1, le=100)] = 50,
):
    cid = _conv_repo.resolver_do_usuario(estudante.id, conversa_id)
    return [
        HistoricoItem(
            id=m.id,
            remetente=m.remetente.value,
            texto=m.texto,
            data_envio=m.data_envio,
            intencao=m.intencao.value if m.intencao else None,
        )
        for m in _conv_repo.listar_mensagens(cid, limite=limite, usuario_id=estudante.id)
    ]
