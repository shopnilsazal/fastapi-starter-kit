# Logging

Structured request/response logging is built into the middleware layer. Every HTTP request automatically produces two log entries — one on arrival, one after the response is sent.

**File:** `app/core/logging.py`

## Logger

A single named logger `"api"` is configured at startup using `settings.LOG_LEVEL` and `settings.LOG_FORMAT`. It writes to stdout and does not propagate to the root logger.

Import it anywhere in the app:

```python
from app.core.logging import logger

logger.info("Something happened")
logger.error("Something went wrong")
```

## Log Levels

Set via the `LOG_LEVEL` environment variable. Accepted values:

`TRACE` · `DEBUG` · `INFO` · `SUCCESS` · `WARNING` · `ERROR` · `CRITICAL`

## Structured Fields

Every log line emitted by `LoggingMiddleware` includes these extra fields from the `LogData` model:

| Field | Description |
|---|---|
| `request_id` | UUID assigned by `RequestIDMiddleware` |
| `user_host` | Client IP address |
| `user_agent` | `User-Agent` request header |
| `path` | Matched route pattern (e.g. `/users/{id}`) |
| `method` | HTTP method |
| `path_params` | Path parameter values |
| `query_params` | Query string as dict |
| `request_data` | Aggregated path params, query params, and payload |
| `response_code` | HTTP status code |
| `response_time` | Request duration in seconds |

## Log Events

| Event | Level | When |
|---|---|---|
| `Request Received` | `INFO` | Immediately after the request enters the middleware |
| `Response Sent` | `INFO` | After the response is fully sent |
| *(exception message)* | `ERROR` | When an unhandled exception is raised |

## Adding Context to Logs

The `LogData` instance is stored on `request.state.log_data`. You can add response-specific information from within a route handler or exception handler:

```python
from starlette.requests import Request

@router.get("/items/{item_id}")
async def get_item(item_id: int, request: Request):
    item = await fetch_item(item_id)
    request.state.log_data.response_data = str(item.id)
    return item
```

This value will appear in the `Response Sent` log entry.
