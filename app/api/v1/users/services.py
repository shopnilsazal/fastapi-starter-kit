from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.api.v1.users.models import User
from app.api.v1.users.repositories import UserRepository
from app.api.v1.users.schemas import UserCreateRequest, UserUpdateRequest
from app.core.errors.api_exception import APIException


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.lower().strip()

    async def _check_username_available(
        self, username: str, exclude_user_id: int | None = None
    ) -> None:
        existing = await self.repo.get_by_username(username)
        if existing and existing.id != exclude_user_id:
            raise APIException(
                msg=f"Username '{username}' is already taken",
                code=40001,
                http_code=HTTP_400_BAD_REQUEST,
            )

    async def _check_email_available(
        self, email: str, exclude_user_id: int | None = None
    ) -> None:
        existing = await self.repo.get_by_email(email)
        if existing and existing.id != exclude_user_id:
            raise APIException(
                msg=f"Email '{email}' is already in use",
                code=40002,
                http_code=HTTP_400_BAD_REQUEST,
            )

    async def create(self, payload: UserCreateRequest) -> User:
        payload.email = self._normalize_email(payload.email)
        await self._check_username_available(payload.username)
        await self._check_email_available(payload.email)
        return await self.repo.create(payload.model_dump())

    async def get(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise APIException(
                msg="User not found",
                code=40401,
                http_code=HTTP_404_NOT_FOUND,
            )
        return user

    async def list_all(
        self, limit: int = 20, offset: int = 0
    ) -> tuple[list[User], int]:
        return await self.repo.list_all(limit, offset)

    async def update(self, user_id: int, payload: UserUpdateRequest) -> User:
        user = await self.get(user_id)

        if payload.email is not None:
            payload.email = self._normalize_email(payload.email)
            await self._check_email_available(payload.email, exclude_user_id=user_id)

        if payload.username is not None:
            await self._check_username_available(
                payload.username, exclude_user_id=user_id
            )

        return await self.repo.update(user, payload.model_dump(exclude_unset=True))

    async def deactivate(self, user_id: int) -> User:
        user = await self.get(user_id)
        if not user.active:
            raise APIException(
                msg="User is already deactivated",
                code=40003,
                http_code=HTTP_400_BAD_REQUEST,
            )
        return await self.repo.deactivate(user)
