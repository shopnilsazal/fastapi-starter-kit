from typing import Optional

from pydantic import EmailStr, Field

from app.core.schema import PydanticModel

# ── Request Schemas ──────────────────────────────────────────────


class UserCreate(PydanticModel):
    """Schema for creating a new user."""

    firstname: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    address: Optional[str] = Field(None, max_length=500)


class UserUpdate(PydanticModel):
    """Schema for updating an existing user. All fields are optional (partial update)."""

    firstname: Optional[str] = Field(None, min_length=1, max_length=100)
    surname: Optional[str] = Field(None, min_length=1, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, max_length=500)


# ── Response Schemas ─────────────────────────────────────────────


class UserResponse(PydanticModel):
    """Schema for a single user in API responses."""

    id: int
    firstname: str
    surname: str
    username: str
    email: EmailStr
    address: Optional[str] = None

    class Config:
        from_attributes = True
