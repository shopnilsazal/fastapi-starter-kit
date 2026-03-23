from unittest.mock import AsyncMock, MagicMock

import pytest

from app.api.v1.users.models import User
from app.api.v1.users.schemas import UserCreate, UserUpdate
from app.api.v1.users.services import UserService
from app.core.errors.api_exception import APIException

# ── Helper: build a fake User object ────────────────────────────


def _make_user(**overrides) -> User:
    defaults = dict(
        id=1,
        firstname="John",
        surname="Doe",
        username="johndoe",
        email="john@example.com",
        address="123 Main St",
        active=True,
    )
    defaults.update(overrides)
    user = MagicMock(spec=User)
    for k, v in defaults.items():
        setattr(user, k, v)
    return user


# ── Helper: build a UserService with a fake Librarian ────────────


def _make_service() -> tuple[UserService, AsyncMock]:
    mock_repo = AsyncMock()
    service = UserService(user_repo=mock_repo)
    return service, mock_repo


# ── CREATE ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_user_success():
    service, repo = _make_service()
    repo.get_by_username.return_value = None
    repo.get_by_email.return_value = None
    repo.create.return_value = _make_user()

    user_in = UserCreate(
        firstname="John",
        surname="Doe",
        username="johndoe",
        email="John@Example.COM",
        address="123 Main St",
    )
    result = await service.create_user(user_in)

    # Email should be normalized to lowercase
    assert user_in.email == "john@example.com"
    repo.create.assert_awaited_once()
    assert result.username == "johndoe"


@pytest.mark.asyncio
async def test_create_user_duplicate_username():
    service, repo = _make_service()
    repo.get_by_username.return_value = _make_user()

    user_in = UserCreate(
        firstname="Jane",
        surname="Doe",
        username="johndoe",
        email="jane@example.com",
    )
    with pytest.raises(APIException) as exc:
        await service.create_user(user_in)

    assert exc.value.status_code == 400
    assert "already taken" in str(exc.value)


@pytest.mark.asyncio
async def test_create_user_duplicate_email():
    service, repo = _make_service()
    repo.get_by_username.return_value = None
    repo.get_by_email.return_value = _make_user()

    user_in = UserCreate(
        firstname="Jane",
        surname="Doe",
        username="janedoe",
        email="john@example.com",
    )
    with pytest.raises(APIException) as exc:
        await service.create_user(user_in)

    assert exc.value.status_code == 400
    assert "already in use" in str(exc.value)


# ── GET ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_user_success():
    service, repo = _make_service()
    repo.get_by_id.return_value = _make_user(id=5, username="alice")

    result = await service.get_user(5)

    repo.get_by_id.assert_awaited_once_with(5)
    assert result.username == "alice"


@pytest.mark.asyncio
async def test_get_user_not_found():
    service, repo = _make_service()
    repo.get_by_id.return_value = None

    with pytest.raises(APIException) as exc:
        await service.get_user(999)

    assert exc.value.status_code == 404
    assert "not found" in str(exc.value)


# ── LIST ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_users():
    service, repo = _make_service()
    repo.get_multi.return_value = [_make_user(id=1), _make_user(id=2)]

    result = await service.list_users(skip=0, limit=10)

    repo.get_multi.assert_awaited_once_with(skip=0, limit=10)
    assert len(result) == 2


# ── UPDATE ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_update_user_success():
    service, repo = _make_service()
    existing = _make_user(id=1)
    updated = _make_user(id=1, firstname="Johnny")
    repo.get_by_id.return_value = existing
    repo.get_by_username.return_value = None
    repo.update.return_value = updated

    user_in = UserUpdate(firstname="Johnny", username="johndoe")
    result = await service.update_user(1, user_in)

    repo.update.assert_awaited_once()
    assert result.firstname == "Johnny"


@pytest.mark.asyncio
async def test_update_user_not_found():
    service, repo = _make_service()
    repo.get_by_id.return_value = None

    user_in = UserUpdate(firstname="Ghost")
    with pytest.raises(APIException) as exc:
        await service.update_user(999, user_in)

    assert exc.value.status_code == 404


# ── DEACTIVATE ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_deactivate_user_success():
    service, repo = _make_service()
    active_user = _make_user(id=1, active=True)
    deactivated = _make_user(id=1, active=False)
    repo.get_by_id.return_value = active_user
    repo.deactivate.return_value = deactivated

    result = await service.deactivate_user(1)

    repo.deactivate.assert_awaited_once_with(active_user)
    assert result.active is False


@pytest.mark.asyncio
async def test_deactivate_user_already_inactive():
    service, repo = _make_service()
    repo.get_by_id.return_value = _make_user(id=1, active=False)

    with pytest.raises(APIException) as exc:
        await service.deactivate_user(1)

    assert exc.value.status_code == 400
    assert "already deactivated" in str(exc.value)
