# FastAPI Starter Kit

A production-ready FastAPI starter template with PostgreSQL, Redis, Docker Compose, and modern Python tooling.

## What's Included

| Category | Technology |
|---|---|
| Framework | FastAPI + Uvicorn |
| Database | PostgreSQL 17 (async via asyncpg + SQLAlchemy 2.0) |
| Cache | Redis 7 (hiredis) |
| Package Manager | uv |
| Python | 3.13+ |
| Serialization | orjson |
| Validation | Pydantic v2 |
| Containerization | Docker + Docker Compose |
| Code Quality | Ruff, pre-commit, gitlint |

## Project Structure

```
fastapi-starter-kit/
├── app/
│   ├── api/                        # API route definitions (add yours here)
│   ├── core/
│   │   ├── config.py               # Settings from environment variables
│   │   ├── logging.py              # Logger setup
│   │   ├── server.py               # FastAPI app factory
│   │   ├── db/
│   │   │   ├── database.py         # Async SQLAlchemy session manager
│   │   │   ├── cache.py            # Redis client
│   │   │   └── models.py           # Declarative ORM base
│   │   ├── errors/
│   │   │   ├── api_exception.py    # Custom APIException
│   │   │   ├── base.py             # BaseCustomError
│   │   │   ├── exception_handlers.py
│   │   │   └── responses.py        # JSONErrorResponse
│   │   ├── middlewares/
│   │   │   ├── logging_middleware.py
│   │   │   ├── request_id_middleware.py
│   │   │   └── utils.py
│   │   └── schema/
│   │       ├── base.py             # BaseResponse, LogData
│   │       └── error.py            # ErrorResponseSchema
│   └── main.py                     # Entrypoint + lifespan
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env
```

## Quick Start

```bash
git clone https://github.com/shopnilsazal/fastapi-starter-kit.git
cd fastapi-starter-kit
docker compose up --build
```

Once running:

- API docs: [http://localhost:8008/docs](http://localhost:8008/docs)
- ReDoc: [http://localhost:8008/redoc](http://localhost:8008/redoc)

See [Installation](getting-started/installation.md) for the full setup guide.
