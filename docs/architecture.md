# Architecture

UniBot separates the browser interface, HTTP routes, application services, domain objects and MySQL persistence.

## Request flow

1. The browser calls FastAPI endpoints, supplying a bearer token where required.
2. Routes validate input and resolve the authenticated user.
3. Services coordinate domain behavior and repository calls.
4. Repositories execute database operations through the connection pool.
5. The response is serialized for the browser.

See [`main.py`](../backend/app/main.py) for router registration and [`connection.py`](../backend/app/db/connection.py) for the connection lifecycle.

## Chatbot behavior

[`Chatbot`](../backend/app/services/chatbot.py) combines intent classification, institutional FAQs, academic data and optional provider calls. [`ProcessadorNLP`](../backend/app/services/processador_nlp.py) classifies supported messages. [`ClaudeService`](../backend/app/services/claude_service.py) wraps the provider SDK and records token usage in its response object.

The tests in [`test_chatbot.py`](../backend/tests/test_chatbot.py) mock repositories and the provider. They validate routing and response composition without connecting to MySQL or making live AI requests.

Chat reads and writes resolve the conversation through the authenticated user's ownership scope. Repository queries also include that user ID, so an internal caller cannot accidentally read or insert a message in another student's conversation. Foreign and missing conversation IDs return the same 404 response. See the [authorization review](chat-authorization.md).

## Domain model

[`usuario.py`](../backend/app/domain/usuario.py) models common user behavior and student, professor and administrator variants. Other modules represent courses, enrollment, grades, deadlines and conversations.

Grade calculations use `Decimal`; see [`nota.py`](../backend/app/domain/nota.py) and its tests.

## Boundaries and tradeoffs

- Mocked domain and service tests are fast, but do not prove live integration behavior.
- Browser-storage authentication tokens require separate evaluation of XSS exposure and session handling before production use.
- The n8n workflow is an integration artifact, not proof of a complete automated deployment.
- Demonstration configuration and records must be replaced before handling real information.

These notes describe the repository inspected on November 1, 2026; they are not a production certification.
