# Middleware

The application uses two custom ASGI middlewares registered in `app/main.py`. FastAPI applies middleware in reverse registration order, so **RequestIDMiddleware runs first**, followed by **LoggingMiddleware**.

## RequestIDMiddleware

**File:** `app/core/middlewares/request_id_middleware.py`

Generates a unique identifier for every incoming request and attaches it to the request state.

**What it does:**

- Generates a `uuid4().hex` string for each request
- Stores it at `scope["state"]["request_id"]`
- Available downstream via `request.state.request_id`

**Usage in route handlers:**

```python
from starlette.requests import Request

@router.get("/example")
async def example(request: Request):
    request_id = request.state.request_id
    ...
```

## LoggingMiddleware

**File:** `app/core/middlewares/logging_middleware.py`

Logs a structured entry on every request received and response sent, including timing information.

**What it captures:**

| Field | Source |
|---|---|
| `request_id` | Set by RequestIDMiddleware |
| `user_host` | `request.client.host` |
| `user_agent` | `User-Agent` header |
| `path` | Matched route pattern (e.g. `/users/{id}`, not `/users/42`) |
| `method` | HTTP method |
| `path_params` | Extracted from the matched route |
| `query_params` | URL query string as dict |
| `response_code` | HTTP status code from the response |
| `response_time` | Duration in seconds (`time.perf_counter()`) |

**Log events emitted:**

1. `Request Received` — logged before the handler runs
2. `Response Sent` — logged after the response is sent (in the `finally` block)
3. If an unhandled exception occurs, the response code is set to `500` and an error-level log is emitted before re-raising.

**LogData schema:**

The middleware populates a `LogData` Pydantic model (`app/core/schema/base.py`) and stores it at `request.state.log_data`. Route handlers and exception handlers can read or update it if needed:

```python
request.state.log_data.response_data = "some value"
```

## Middleware Utilities

**File:** `app/core/middlewares/utils.py`

| Function | Purpose |
|---|---|
| `get_matching_route_path(request)` | Returns the route pattern (e.g. `/items/{id}`) rather than the actual URL path |
| `get_path_params(request)` | Returns a dict of path parameters extracted from the matched route |

These are used by `LoggingMiddleware` to log clean route patterns instead of raw URLs, which keeps log aggregation consistent across different parameter values.
