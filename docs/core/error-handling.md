# Error Handling

The project provides a consistent JSON error response format for all API errors, backed by two exception handlers registered in `app/core/server.py`.

## Error Response Format

All error responses follow this structure:

```json
{
  "success": false,
  "code": 50001,
  "data": {
    "error_message": "Something went wrong",
    "details": null
  }
}
```

## Raising API Errors

Use `APIException` to return a structured error response from anywhere in your application:

```python
from app.core.errors.api_exception import APIException

raise APIException(
    msg="User not found",
    code=40401,
    http_code=404,
)
```

| Parameter | Type | Description |
|---|---|---|
| `msg` | `str` | Human-readable error message returned in `data.error_message` |
| `code` | `int` | Application-level error code returned in the response body |
| `http_code` | `int` | HTTP status code (default: `500`) |
| `headers` | `dict` | Optional response headers |

## Exception Handlers

### APIException Handler

Catches `APIException` and returns a `JSONErrorResponse` with the structured body above.

### RequestValidationError Handler

Catches Pydantic validation errors (e.g. when request body or query parameters fail schema validation) and returns a `422 Unprocessable Entity` with validation details.

## Custom Error Classes

For internal errors that are not exposed directly to the client, extend `BaseCustomError`:

```python
from app.core.errors.base import BaseCustomError

class InsufficientPermissionsError(BaseCustomError):
    def __init__(self):
        super().__init__(msg="Insufficient permissions", code=40301)
```

Catch these internally and convert to `APIException` before they reach the handler layer.

## Schemas

**`ErrorDataSchema`** (`app/core/schema/error.py`)

```python
class ErrorDataSchema(PydanticModel):
    error_message: str = "Internal Server Error"
    details: Optional[Any] = None
```

**`ErrorResponseSchema`** (`app/core/schema/error.py`)

```python
class ErrorResponseSchema(BaseResponse):
    success: bool = False
    code: int = 50001
    data: ErrorDataSchema
```
