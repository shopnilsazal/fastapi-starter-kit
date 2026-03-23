# Architecture Overview

## Request Lifecycle

Every HTTP request passes through the following layers in order:

```
Client
  │
  ▼
Starlette Error Middleware        (catches unhandled exceptions)
  │
  ▼
RequestIDMiddleware               (generates a UUID for the request)
  │
  ▼
LoggingMiddleware                 (logs request metadata + timing)
  │
  ▼
CORSMiddleware                    (handles CORS preflight/headers)
  │
  ▼
Route Handler                     (your business logic)
  │
  ▼
Exception Handlers                (APIException, RequestValidationError)
  │
  ▼
Client
```

## Application Factory

The FastAPI instance is created by `create_fastapi_app()` in `app/core/server.py`. It is not instantiated at module level — instead it is built with a lifespan context manager that manages startup and shutdown of external resources.

**`app/main.py`** wires everything together:

1. Defines the `app_lifespan` async context manager
2. Calls `create_fastapi_app()` passing config values and lifespan
3. Registers `LoggingMiddleware` and `RequestIDMiddleware`

**Startup sequence:**

1. Connect to Redis (`connect_cache_db()`)
2. Application is ready to serve requests

**Shutdown sequence:**

1. Disconnect from Redis (`disconnect_cache_db()`)
2. Close the SQLAlchemy engine (`session_manager.close()`)

## Adding API Routes

The `app/api/` directory is the intended home for route definitions. Register routers in `app/main.py`:

```python
from app.api.your_module import router

app.include_router(router, prefix=settings.API_V1_PREFIX)
```

## Key Design Decisions

**Async-first** — SQLAlchemy uses `create_async_engine` with the `asyncpg` driver. Redis uses the async `redis.asyncio` client. All I/O is non-blocking.

**Pydantic v2 for settings** — `pydantic-settings` validates and coerces all environment variables at startup, failing fast if required values are missing or invalid.

**orjson as default response class** — All responses use `ORJSONResponse` instead of the standard `JSONResponse`, providing faster serialization with native support for `datetime`, `UUID`, and `bytes`.

**Structured logging** — Every log line includes `request_id`, `path`, `method`, `response_code`, and `response_time` as structured fields, making logs easy to query in any log aggregator.
