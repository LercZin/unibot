from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Nota:
    id: int
    matricula_id: int
    tipo: str
    valor: Decimal
    peso: Decimal
    data: date


def calcular_media_ponderada(notas: list[Nota]) -> Decimal:
    """Média ponderada das notas pelo peso. Retorna 0 quando não há notas."""
    if not notas:
        return Decimal("0")
    soma_pesos = sum((n.peso for n in notas), Decimal("0"))
    if soma_pesos == 0:
        return Decimal("0")
    soma_pond = sum((n.valor * n.peso for n in notas), Decimal("0"))
    return (soma_pond / soma_pesos).quantize(Decimal("0.01"))


def classificar_situacao(media: Decimal, nota_aprovacao: Decimal = Decimal("6.0")) -> str:
    if media >= nota_aprovacao:
        return "aprovado"
    if media >= nota_aprovacao - Decimal("2.0"):
        return "em_recuperacao"
    return "em_risco"
