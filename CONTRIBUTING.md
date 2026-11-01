# Development guide

Read the [README](README.md) for local setup and the [architecture notes](docs/architecture.md) for component responsibilities.

## Before changing the project

- Use a local development database with demonstration data.
- Keep environment files, tokens and database exports out of Git.
- Preserve contributor credits and the academic nature of the project.
- Report verification scope; mocked tests are not live integration tests.

## Check a change

Install dependencies from `backend/requirements.txt`, then run:

```bash
python -m pytest backend/tests -q
node --test frontend/tests/*.test.cjs
```

Use tests that exercise changed behavior. Database, authentication and browser changes also need appropriate integration or manual verification beyond this suite.

## Pull requests

Explain the problem, resulting behavior, verification and limitations. Use descriptive commits and avoid unrelated formatting changes.

Do not attach real student records, credentials or screenshots containing personal information to issues or pull requests.
