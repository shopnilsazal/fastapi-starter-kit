from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.repository import UserRepository
from app.api.v1.users.schemas import UserCreate, UserResponse, UserUpdate
from app.api.v1.users.services import UserService
from app.core.db.database import get_db_session

# ── Dependency chain ─────────────────────────────────────────────
# Session → Repository → Service  (handed to each view automatically)


def get_user_service(session: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(UserRepository(session))


# ── Views (The Chef's dishes) ───────────────────────────────────


async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.create_user(user_in)
    return UserResponse.model_validate(user)


async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.get_user(user_id)
    return UserResponse.model_validate(user)


async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    users = await service.list_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


async def update_user(
    user_id: int,
    user_in: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.update_user(user_id, user_in)
    return UserResponse.model_validate(user)


async def deactivate_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.deactivate_user(user_id)
    return UserResponse.model_validate(user)
