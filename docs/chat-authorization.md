# Chat authorization and regression checks

## Boundary

A student's authenticated identity is supplied by the existing `somente_estudante` dependency. Possessing the student role does not grant access to every conversation ID.

- Explicit conversation IDs are resolved using both conversation ID and authenticated user ID.
- History queries join the conversation owner, and message inserts select only a conversation owned by that user.
- A missing or foreign conversation receives the same 404 response.
- A denied send creates no message and makes no AI-provider request.
- Omitting the ID resolves or creates the authenticated student's own conversation.
- Conversation IDs must be positive; history requests accept between 1 and 100 messages.
- Timestamp ties are ordered by message ID, preserving stable chronology.

The widget uses `historicoChat()` for chat messages. Academic records retain the separate `historico()` client method.

## Verification

[`test_chat_authorization.py`](../backend/tests/test_chat_authorization.py) sends HTTP requests through the chat router with two distinct student identities, exercises repository SQL, and checks read/write denials and lack of side effects. It also checks unknown IDs, new-conversation ownership and input bounds.

For isolation, authentication is supplied by a test dependency and SQL is executed through an in-memory SQLite adapter. These tests validate the object-authorization boundary; they do not exercise real JWT authentication, the MySQL driver, provider calls or a production deployment.

[`widget.test.cjs`](../frontend/tests/widget.test.cjs) executes the actual browser API client and widget together with HTTP and DOM doubles. It verifies that chat messages are fetched from the chat endpoint and rendered, rather than silently falling back after receiving academic-record data.

Run all checks from the repository root:

```bash
python -m pytest backend/tests -q
node --test frontend/tests/*.test.cjs
```

The November 1, 2026 checks passed with 75 Python tests and 11 JavaScript tests. This maintenance adds ownership checks and regression coverage while preserving the academic team credits and existing application scope.
