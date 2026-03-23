from typing import Optional

from pydantic import ConfigDict, EmailStr, Field

from app.core.schema import PydanticModel
from app.core.schema.base import BaseResponse

# ── Request Schemas ──────────────────────────────────────────────


class UserCreateRequest(PydanticModel):
    firstname: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    address: Optional[str] = Field(None, max_length=500)


class UserUpdateRequest(PydanticModel):
    firstname: Optional[str] = Field(None, min_length=1, max_length=100)
    surname: Optional[str] = Field(None, min_length=1, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, max_length=500)


# ── Response Schemas ─────────────────────────────────────────────


class UserResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    firstname: str
    surname: str
    username: str
    email: EmailStr
    address: Optional[str] = None
    active: bool


class UserListResponse(PydanticModel):
    items: list[UserResponse]
    total: int


class SingleUserAPIResponse(BaseResponse):
    success: bool = True
    code: int = 200
    data: UserResponse


class UserListAPIResponse(BaseResponse):
    success: bool = True
    code: int = 200
    data: UserListResponse
