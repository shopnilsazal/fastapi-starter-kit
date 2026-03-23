from typing import Sequence

from app.api.v1.users.models import User
from app.api.v1.users.repository import UserRepository
from app.api.v1.users.schemas import UserCreate, UserUpdate
from app.core.errors.api_exception import APIException


class UserService:
    """
    The Referee — enforces all business rules before letting
    the Repository (Librarian) touch the database.
    """

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    # ── Business-rule helpers ────────────────────────────────────

    @staticmethod
    def _normalize_email(email: str) -> str:
        """Lowercase the email so 'Bob@Email.COM' and 'bob@email.com' are the same person."""
        return email.lower().strip()

    async def _check_username_available(
        self, username: str, exclude_user_id: int | None = None
    ) -> None:
        """Blow the whistle if someone already has this username."""
        existing = await self.user_repo.get_by_username(username)
        if existing and existing.id != exclude_user_id:
            raise APIException(
                msg=f"Username '{username}' is already taken",
                code=400,
                http_code=400,
            )

    async def _check_email_available(
        self, email: str, exclude_user_id: int | None = None
    ) -> None:
        """Blow the whistle if someone already has this email."""
        existing = await self.user_repo.get_by_email(email)
        if existing and existing.id != exclude_user_id:
            raise APIException(
                msg=f"Email '{email}' is already in use",
                code=400,
                http_code=400,
            )

    # ── Public methods (called by the Waiter / Routes) ───────────

    async def create_user(self, user_in: UserCreate) -> User:
        """
        Create a new user after enforcing:
        1. Normalize the email to lowercase
        2. Username must be unique
        3. Email must be unique
        """
        # Normalize
        user_in.email = self._normalize_email(user_in.email)

        # Uniqueness checks
        await self._check_username_available(user_in.username)
        await self._check_email_available(user_in.email)

        # All rules passed — tell the Librarian to save
        return await self.user_repo.create(user_in)

    async def get_user(self, user_id: int) -> User:
        """Retrieve a single user or raise 404."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise APIException(
                msg="User not found",
                code=404,
                http_code=404,
            )
        return user

    async def list_users(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        """Retrieve a paginated list of users."""
        return await self.user_repo.get_multi(skip=skip, limit=limit)

    async def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        """
        Update an existing user after enforcing:
        1. The user must exist
        2. If changing email — normalize it and ensure it's not taken
        3. If changing username — ensure it's not taken
        """
        user = await self.get_user(user_id)

        # Only run uniqueness checks for fields being changed
        if user_in.email is not None:
            user_in.email = self._normalize_email(user_in.email)
            await self._check_email_available(user_in.email, exclude_user_id=user_id)

        if user_in.username is not None:
            await self._check_username_available(
                user_in.username, exclude_user_id=user_id
            )

        return await self.user_repo.update(user, user_in)

    async def deactivate_user(self, user_id: int) -> User:
        """Deactivate a user — they must exist and be currently active."""
        user = await self.get_user(user_id)
        if not user.active:
            raise APIException(
                msg="User is already deactivated",
                code=400,
                http_code=400,
            )
        return await self.user_repo.deactivate(user)
