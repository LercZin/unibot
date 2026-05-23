from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import ClassVar


class TipoUsuario(str, Enum):
    ESTUDANTE = "estudante"
    PROFESSOR = "professor"
    ADMINISTRADOR = "administrador"


@dataclass
class Usuario(ABC):
    """Classe abstrata base da hierarquia de usuários.

    Encapsula os atributos comuns a todos os perfis e define o contrato
    (`tipo` e `permissoes`) que cada subclasse deve cumprir — exemplos
    diretos dos pilares de encapsulamento, herança, polimorfismo e
    abstração estudados em POO II.
    """

    id: int
    nome: str
    email: str
    senha_hash: str
    data_cadastro: datetime
    ativo: bool = True

    tipo: ClassVar[TipoUsuario]

    @abstractmethod
    def permissoes(self) -> set[str]:
        """Lista de permissões do perfil — sobrescrita em cada subclasse."""

    def pode(self, acao: str) -> bool:
        return acao in self.permissoes()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, nome={self.nome!r})"


@dataclass
class Estudante(Usuario):
    matricula: str = ""
    curso: str = ""
    semestre: int = 1

    tipo: ClassVar[TipoUsuario] = TipoUsuario.ESTUDANTE

    def permissoes(self) -> set[str]:
        return {"chat:enviar", "chat:historico", "nota:ler", "prazo:ler", "material:ler"}


@dataclass
class Professor(Usuario):
    registro_docente: str = ""
    titulacao: str = ""

    tipo: ClassVar[TipoUsuario] = TipoUsuario.PROFESSOR

    def permissoes(self) -> set[str]:
        return {
            "disciplina:gerenciar",
            "prazo:gerenciar",
            "nota:gerenciar",
            "material:gerenciar",
            "relatorio:disciplina",
        }


@dataclass
class Administrador(Usuario):
    departamento: str = "TI"

    tipo: ClassVar[TipoUsuario] = TipoUsuario.ADMINISTRADOR

    def permissoes(self) -> set[str]:
        return {
            "usuario:gerenciar",
            "base_conhecimento:gerenciar",
            "relatorio:geral",
            "disciplina:gerenciar",
        }


def construir_usuario(linha: dict) -> Usuario:
    """Factory que constrói a subclasse correta a partir de uma linha do banco.

    Espera as colunas de `usuario` mais as colunas do JOIN com a tabela
    específica do perfil. Demonstra polimorfismo: o resto do código trabalha
    com `Usuario` e ignora qual subclasse foi instanciada.
    """
    tipo = TipoUsuario(linha["tipo"])
    base = dict(
        id=linha["id"],
        nome=linha["nome"],
        email=linha["email"],
        senha_hash=linha["senha_hash"],
        data_cadastro=linha["data_cadastro"],
        ativo=bool(linha["ativo"]),
    )
    if tipo == TipoUsuario.ESTUDANTE:
        return Estudante(
            **base,
            matricula=linha.get("matricula") or "",
            curso=linha.get("curso") or "",
            semestre=int(linha.get("semestre") or 1),
        )
    if tipo == TipoUsuario.PROFESSOR:
        return Professor(
            **base,
            registro_docente=linha.get("registro_docente") or "",
            titulacao=linha.get("titulacao") or "",
        )
    return Administrador(**base, departamento=linha.get("departamento") or "TI")
