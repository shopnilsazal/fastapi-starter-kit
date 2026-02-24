# FastAPI Starter Kit

A production-ready FastAPI starter template with PostgreSQL, Redis, Docker Compose, and modern Python tooling.

## Tech Stack

- **Framework** — [FastAPI](https://fastapi.tiangolo.com/) with Uvicorn
- **Database** — PostgreSQL 17 (via asyncpg + SQLAlchemy)
- **Cache** — Redis 7
- **Package Manager** — [uv](https://docs.astral.sh/uv/)
- **Python** — 3.14+

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- [Git](https://git-scm.com/)

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fastapi-starter-kit
```

### 2. Configure Environment Variables

Create a `.env` file in the project root (a default one is included):

```env
POSTGRES_USER=app_user
POSTGRES_PASSWORD=HelloDB!234
POSTGRES_DB=app_db
DB_HOST=database
DB_PORT=5432
```

> [!IMPORTANT]
> Change `POSTGRES_PASSWORD` to a strong, unique password before deploying to any non-local environment.

### 3. Build & Start the Services

```bash
docker compose up --build
```

This will spin up three services:

| Service      | Description       | Host Port |
|--------------|-------------------|-----------|
| **backend**  | FastAPI app       | `8008`    |
| **database** | PostgreSQL 17     | `5432`    |
| **redis**    | Redis 7           | `6380`    |

The backend waits for both PostgreSQL and Redis to pass their health checks before starting.

### 4. Verify It's Running

Open your browser or use `curl`:

```bash
# Interactive API docs
open http://localhost:8008/docs

# Health check
curl http://localhost:8008/
```

## Common Commands

```bash
# Start all services (detached)
docker compose up -d --build

# View logs
docker compose logs -f            # all services
docker compose logs -f backend    # backend only

# Stop all services
docker compose down

# Stop and remove volumes (⚠️ deletes database data)
docker compose down -v

# Rebuild only the backend
docker compose build backend

# Restart a single service
docker compose restart backend

# Open a shell in the running backend container
docker compose exec backend bash
```

## Project Structure

```
fastapi-starter-kit/
├── app/
│   ├── api/              # API route definitions
│   ├── core/             # Config, database, middleware, server setup
│   └── main.py           # Application entrypoint
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Service orchestration
├── pyproject.toml        # Python dependencies (managed by uv)
├── uv.lock               # Lockfile
├── ruff.toml             # Linter / formatter config
└── .env                  # Environment variables
```

## Local Development (Without Docker)

If you prefer running outside Docker, make sure you have Python 3.14+ and `uv` installed:

```bash
# Install dependencies
uv sync

# Run the dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8008
```

> [!NOTE]
> You'll need a running PostgreSQL and Redis instance accessible from your machine. Update `DB_HOST` in `.env` to `localhost` (instead of `database`) when running outside Docker.

## License

This project is licensed under the [MIT License](LICENSE).
