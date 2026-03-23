# Database

The project uses **SQLAlchemy 2.0** with the async `asyncpg` driver for non-blocking PostgreSQL access.

**File:** `app/core/db/database.py`

## DatabaseSessionManager

`DatabaseSessionManager` wraps the SQLAlchemy async engine and session factory. A single instance (`session_manager`) is created at module load using `settings.DB_URL`.

### Methods

**`async close()`**

Disposes of the engine and clears internal state. Called during application shutdown.

**`async connect()`** *(async context manager)*

Yields a raw `AsyncConnection` for executing SQL directly:

```python
async with session_manager.connect() as conn:
    result = await conn.execute(text("SELECT 1"))
```

**`async session()`** *(async context manager)*

Yields an `AsyncSession` for ORM operations. Rolls back automatically on exception and closes when the block exits:

```python
async with session_manager.session() as session:
    session.add(my_model_instance)
    await session.commit()
```

## Dependency Injection

Use `get_db_session` as a FastAPI dependency to get a session scoped to the request:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.db.database import get_db_session

@router.get("/items")
async def list_items(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Item))
    return result.scalars().all()
```

The session is automatically rolled back on error and closed after the response.

## Defining Models

Inherit from `BaseModel` in `app/core/db/models.py`:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db.models import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

## Connection URL

The URL is assembled automatically from environment variables by the `Settings` class:

```
postgresql+asyncpg://<POSTGRES_USER>:<POSTGRES_PASSWORD>@<DB_HOST>:<DB_PORT>/<POSTGRES_DB>
```

You never need to set `DB_URL` directly — configure the individual variables in `.env`.
