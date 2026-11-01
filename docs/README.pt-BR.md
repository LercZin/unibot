# UniBot

Assistente acadêmico inteligente com chatbot (PLN) — projeto da disciplina de POO II / Chatbot da Anhanguera.

## Stack

- **Backend**: Python 3.11+, FastAPI, mysql-connector-python, Pydantic, Anthropic SDK
- **Banco**: MySQL 8.0
- **Orquestração**: n8n (workflows visuais)
- **IA**: Claude (Anthropic) — modelo `claude-sonnet-4-6`
- **Frontend**: HTML5 + CSS3 + JS vanilla + Bootstrap 5

## Estrutura

```
UniBot/
├── backend/             # API FastAPI
│   ├── app/
│   │   ├── core/        # config, segurança, exceções
│   │   ├── db/          # conexão MySQL e repositórios (DAO)
│   │   ├── domain/      # classes POO do domínio (Usuario, Estudante, ...)
│   │   ├── routers/     # endpoints REST
│   │   ├── schemas/     # modelos Pydantic (entrada/saída)
│   │   ├── services/    # regras de negócio (Chatbot, NLP, Claude)
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── database/            # schema.sql + seed.sql
├── frontend/            # login + chat (Bootstrap 5)
├── n8n/workflows/       # exportação dos fluxos do n8n
└── docker-compose.yml
```

## Como rodar

### 1) Banco

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql   # opcional: dados de teste
```

### 2) Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy ..\.env.example ..\.env    # e preencha
uvicorn app.main:app --reload
```

API em `http://localhost:8000` — docs em `/docs`.

### 3) Frontend

Servir a pasta `frontend/` (ex.: `python -m http.server 8080` dentro dela) ou abrir `index.html` direto.

### 4) n8n (opcional nessa fase)

```bash
docker run -it --rm -p 5678:5678 n8nio/n8n
```

Importe os workflows de `n8n/workflows/`.

## Mapeamento de requisitos

Cada requisito funcional (RF01–RF15) da documentação está endereçado em uma rota ou serviço:

| Requisito | Local |
|---|---|
| RF01, RF13 | `routers/usuarios.py`, `routers/admin.py` |
| RF02 | `routers/auth.py` |
| RF03, RF04, RF05, RF09 | `services/chatbot.py`, `services/processador_nlp.py`, `services/claude_service.py` |
| RF06, RF11 | `routers/prazos.py` |
| RF07, RF11 | `routers/notas.py` |
| RF08, RF11 | `routers/materiais.py` |
| RF10 | `routers/chat.py` (histórico) |
| RF12 | `routers/admin.py` (relatórios) |
| RF14 | `routers/admin.py` (base de conhecimento) |
| RF15 | logs em `core/logging.py` |

## Integrantes

- Lucas Emanuel Ramos Carvalho
- Pedro Henrick Silva de Oliveira
- Danilo da Silva Portela
