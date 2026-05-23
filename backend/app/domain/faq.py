from dataclasses import dataclass


@dataclass
class FaqItem:
    id: int
    categoria: str
    pergunta: str
    resposta: str
    link: str | None = None

    def formatar(self) -> str:
        if self.link:
            return f"{self.resposta}\n\n🔗 {self.link}"
        return self.resposta
