import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.api.events.models import Event
from app.api.events.schemas import EventCreateRequest, EventUpdateRequest
from app.api.events.services import EventService
from app.core.errors.api_exception import APIException


def make_event(**kwargs) -> Event:
    defaults = dict(
        id=uuid.uuid4(),
        title="Test Event",
        description=None,
        location=None,
        start_at=datetime(2026, 6, 1, 10, 0, tzinfo=timezone.utc),
        end_at=datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc),
        is_all_day=False,
        status="scheduled",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        updated_at=None,
    )
    defaults.update(kwargs)
    event = MagicMock(spec=Event)
    for k, v in defaults.items():
        setattr(event, k, v)
    return event


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def service(mock_session):
    return EventService(mock_session)


# --- create ---


@pytest.mark.asyncio
async def test_create_event(service):
    payload = EventCreateRequest(
        title="Birthday Party",
        start_at=datetime(2026, 6, 1, 10, 0, tzinfo=timezone.utc),
        end_at=datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc),
    )
    expected = make_event(title="Birthday Party")
    service.repo.create = AsyncMock(return_value=expected)

    result = await service.create(payload)
    assert result.title == "Birthday Party"


# --- get ---


@pytest.mark.asyncio
async def test_get_event_found(service):
    event = make_event()
    service.repo.get_by_id = AsyncMock(return_value=event)

    result = await service.get(event.id)
    assert result.id == event.id


@pytest.mark.asyncio
async def test_get_event_not_found(service):
    service.repo.get_by_id = AsyncMock(return_value=None)

    with pytest.raises(APIException) as exc:
        await service.get(uuid.uuid4())
    assert exc.value.status_code == 404
    assert exc.value.code == 40401


# --- list ---


@pytest.mark.asyncio
async def test_list_events(service):
    events = [make_event(), make_event()]
    service.repo.list_all = AsyncMock(return_value=(events, 2))

    result, total = await service.list_all()
    assert total == 2
    assert len(result) == 2


# --- update ---


@pytest.mark.asyncio
async def test_update_event(service):
    event = make_event()
    updated = make_event(title="Updated")
    service.repo.get_by_id = AsyncMock(return_value=event)
    service.repo.update = AsyncMock(return_value=updated)

    payload = EventUpdateRequest(title="Updated")
    result = await service.update(event.id, payload)
    assert result.title == "Updated"


# --- delete ---


@pytest.mark.asyncio
async def test_delete_event(service):
    event = make_event()
    service.repo.get_by_id = AsyncMock(return_value=event)
    service.repo.delete = AsyncMock()

    await service.delete(event.id)
    service.repo.delete.assert_called_once_with(event)


# --- schema validation ---


def test_invalid_date_range():
    with pytest.raises(ValueError):
        EventCreateRequest(
            title="Bad Event",
            start_at=datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc),
            end_at=datetime(2026, 6, 1, 10, 0, tzinfo=timezone.utc),
        )
