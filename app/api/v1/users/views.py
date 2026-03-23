from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.models import User
from app.api.v1.users.schemas import (
    SingleUserAPIResponse,
    UserCreateRequest,
    UserListAPIResponse,
    UserListResponse,
    UserResponse,
    UserUpdateRequest,
)
from app.api.v1.users.services import UserService
from app.core.db.database import get_db_session


def single_user_response(user: User) -> SingleUserAPIResponse:
    return SingleUserAPIResponse(data=UserResponse.model_validate(user))


def user_list_response(users: list[User], total: int) -> UserListAPIResponse:
    return UserListAPIResponse(
        data=UserListResponse(
            items=[UserResponse.model_validate(u) for u in users],
            total=total,
        )
    )


async def create_user(
    payload: UserCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> SingleUserAPIResponse:
    user = await UserService(session).create(payload)
    return single_user_response(user)


async def list_users(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
) -> UserListAPIResponse:
    users, total = await UserService(session).list_all(limit, offset)
    return user_list_response(users, total)


async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> SingleUserAPIResponse:
    user = await UserService(session).get(user_id)
    return single_user_response(user)


async def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> SingleUserAPIResponse:
    user = await UserService(session).update(user_id, payload)
    return single_user_response(user)


async def deactivate_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> SingleUserAPIResponse:
    user = await UserService(session).deactivate(user_id)
    return single_user_response(user)
