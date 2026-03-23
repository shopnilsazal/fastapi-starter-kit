# Configuration

All configuration is driven by environment variables, loaded from the `.env` file via Pydantic Settings (`app/core/config.py`).

!!! warning
    All variable names are **case-sensitive**.

## Environment Variables

### Database

| Variable | Default | Description |
|---|---|---|
| `POSTGRES_USER` | `app_user` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `Pass1234` | PostgreSQL password — **change this in production** |
| `POSTGRES_DB` | `app_db` | PostgreSQL database name |
| `DB_HOST` | `database` | Hostname (`database` in Docker, `localhost` locally) |
| `DB_PORT` | `5432` | PostgreSQL port |

### Cache

| Variable | Default | Description |
|---|---|---|
| `REDIS_HOST` | `redis` | Hostname (`redis` in Docker, `localhost` locally) |
| `REDIS_PORT` | `6379` | Redis port |
| `REDIS_PASS` | `fastapithing` | Redis password |

### Application

| Variable | Default | Description |
|---|---|---|
| `DEBUG` | `false` | Enables debug mode when set to `true` |
| `TIME_ZONE` | `Asia/Dhaka` | Timezone used by the container |
| `LOG_LEVEL` | `DEBUG` | One of: `TRACE`, `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL` |
| `LOG_FORMAT` | *(structured format string)* | Python `logging` format string; defaults to a structured line with all request/response fields |

## Default `.env`

```env
POSTGRES_USER=app_user
POSTGRES_PASSWORD=Pass1234
POSTGRES_DB=app_db
DB_HOST=database
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASS=fastapithing

TIME_ZONE=Asia/Dhaka
LOG_LEVEL=DEBUG
```

## Settings Class

The `Settings` class in `app/core/config.py` validates all variables at startup and exposes them as typed attributes.

Notable computed fields:

- **`DB_URL`** — constructed automatically as `postgresql+asyncpg://user:password@host:port/db`. You never need to set this manually.
- **`CORS_ORIGINS`** — accepts a JSON string or a Python list. Defaults to `["127.0.0.1", "0.0.0.0"]`.

Access settings anywhere in the app:

```python
from app.core.config import settings

print(settings.DB_URL)
print(settings.LOG_LEVEL)
```
