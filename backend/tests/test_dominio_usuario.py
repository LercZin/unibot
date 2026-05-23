"""Testes do modelo de domínio — exercitam herança e polimorfismo (POO II)."""
from datetime import datetime

import pytest

from app.domain.usuario import (
    Administrador,
    Estudante,
    Professor,
    TipoUsuario,
    Usuario,
    construir_usuario,
)


def _base(**extras):
    return dict(
        id=1, nome="Fulano", email="x@y.z", senha_hash="h",
        data_cadastro=datetime(2026, 1, 1), ativo=True, **extras,
    )


def test_classes_concretas_herdam_de_usuario():
    e = Estudante(**_base(matricula="2025001", curso="ADS", semestre=1))
    assert isinstance(e, Usuario)


def test_polimorfismo_permissoes():
    e = Estudante(**_base(matricula="m", curso="c", semestre=1))
    p = Professor(**_base(registro_docente="D", titulacao="Mestre"))
    a = Administrador(**_base())

    assert e.pode("chat:enviar")
    assert not e.pode("usuario:gerenciar")
    assert p.pode("disciplina:gerenciar")
    assert a.pode("usuario:gerenciar")


def test_nao_pode_instanciar_usuario_abstrato():
    with pytest.raises(TypeError):
        Usuario(**_base())


def test_factory_constroi_subclasse_correta():
    linha = _base(tipo="estudante", matricula="2025001", curso="ADS", semestre=2)
    u = construir_usuario(linha)
    assert isinstance(u, Estudante)
    assert u.tipo == TipoUsuario.ESTUDANTE
    assert u.semestre == 2
