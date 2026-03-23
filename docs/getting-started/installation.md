# Installation

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) v2+
- [Git](https://git-scm.com/)

## With Docker (Recommended)

### 1. Clone the repository

```bash
git clone https://github.com/shopnilsazal/fastapi-starter-kit.git
cd fastapi-starter-kit
```

### 2. Configure environment variables

A default `.env` file is included. Review it before starting — at minimum change `POSTGRES_PASSWORD` for any non-local environment.

See [Configuration](configuration.md) for all available variables.

### 3. Build and start

```bash
docker compose up --build
```

This starts three services and waits for health checks to pass before the backend comes up:

| Service | Description | Host Port |
|---|---|---|
| `backend` | FastAPI app | `8008` |
| `database` | PostgreSQL 17 | `5432` |
| `redis` | Redis 7 | `6380` |

### 4. Verify

```bash
# Interactive API docs
open http://localhost:8008/docs

# Health check
curl http://localhost:8008/
```

## Common Docker Commands

```bash
# Start detached
docker compose up -d --build

# Follow logs
docker compose logs -f backend

# Stop all services
docker compose down

# Stop and wipe database data
docker compose down -v

# Rebuild only the backend
docker compose build backend

# Restart the backend
docker compose restart backend

# Open a shell in the container
docker compose exec backend bash
```

## Without Docker (Local Development)

**Prerequisites:** Python 3.14+, a running PostgreSQL 17 instance, and Redis 7.

### 1. Install dependencies

```bash
uv sync
```

### 2. Update `.env`

When running outside Docker, point the services at localhost:

```env
DB_HOST=localhost
REDIS_HOST=localhost
```

### 3. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8008
```

## Setting Up Pre-commit Hooks

Install the hooks once after cloning so linting and commit-message checks run automatically:

```bash
uv sync
pre-commit install
pre-commit install --hook-type commit-msg
```

| Hook | Stage | Purpose |
|---|---|---|
| `ruff` | `commit` | Lints Python files and auto-fixes issues |
| `ruff-format` | `commit` | Formats Python files (Black-compatible) |
| `gitlint` | `commit-msg` | Enforces Conventional Commits style |

Run manually at any time:

```bash
pre-commit run --all-files
```
