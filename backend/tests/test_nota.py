from datetime import date
from decimal import Decimal

from app.domain.nota import Nota, calcular_media_ponderada, classificar_situacao


def _nota(valor, peso):
    return Nota(id=0, matricula_id=1, tipo="AV", valor=Decimal(str(valor)),
                peso=Decimal(str(peso)), data=date(2026, 1, 1))


def test_media_vazia_eh_zero():
    assert calcular_media_ponderada([]) == Decimal("0")


def test_media_ponderada():
    notas = [_nota(8, 1), _nota(6, 2)]
    # (8*1 + 6*2) / 3 = 20/3 = 6,67
    assert calcular_media_ponderada(notas) == Decimal("6.67")


def test_classificar_situacao():
    assert classificar_situacao(Decimal("7.0")) == "aprovado"
    assert classificar_situacao(Decimal("5.0")) == "em_recuperacao"
    assert classificar_situacao(Decimal("2.0")) == "em_risco"
