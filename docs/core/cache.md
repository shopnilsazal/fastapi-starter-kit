# Cache

The project uses **Redis 7** via the async `redis.asyncio` client with the `hiredis` C-extension for faster parsing.

**File:** `app/core/db/cache.py`

## Connection

The Redis client is initialised on application startup via the lifespan in `app/main.py`:

```python
await connect_cache_db()   # startup
await disconnect_cache_db() # shutdown
```

`connect_cache_db()` creates a connection pool and a Redis client using the values from `settings` (`REDIS_HOST`, `REDIS_PORT`, `REDIS_PASS`).

### Connection Pool Settings

| Setting | Value |
|---|---|
| Database index | `0` |
| Health check interval | 15 seconds |
| Socket timeout | 5 seconds |
| Retry strategy | Exponential backoff, 3 retries |
| Retry on | `BusyLoadingError`, `ConnectionError`, `TimeoutError` |
| Response decoding | UTF-8 (`decode_responses=True`) |

## Using the Cache Client

Inject the Redis client as a FastAPI dependency with `get_cache_client`:

```python
from fastapi import Depends
from app.core.db.cache import CacheClient, get_cache_client

@router.get("/example")
async def example(cache: CacheClient = Depends(get_cache_client)):
    await cache.set("key", "value", ex=60)
    value = await cache.get("key")
    return {"value": value}
```

`CacheClient` is a type alias for `redis.asyncio.Redis`, so your editor's autocomplete will work normally.

## Direct Access

If you need the client outside of a route handler:

```python
from app.core.db.cache import cache_db

client = cache_db.client
await client.set("key", "value")
```

!!! note
    `cache_db.client` is `None` until `connect_cache_db()` has been called (i.e. after application startup).
