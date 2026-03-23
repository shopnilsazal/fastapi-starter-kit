import uuid
from datetime import datetime
from typing import Optional

from fastapi import Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.events.models import Event
from app.api.v1.events.schemas import (
    EventCreateRequest,
    EventListAPIResponse,
    EventListResponse,
    EventResponse,
    EventStatus,
    EventUpdateRequest,
    SingleEventAPIResponse,
)
from app.api.v1.events.services import EventService
from app.core.db.database import get_db_session


def single_event_response(event: Event) -> SingleEventAPIResponse:
    return SingleEventAPIResponse(data=EventResponse.model_validate(event))


def event_list_response(events: list[Event], total: int) -> EventListAPIResponse:
    return EventListAPIResponse(
        data=EventListResponse(
            items=[EventResponse.model_validate(e) for e in events],
            total=total,
        )
    )


async def create_event_handler(
    payload: EventCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> SingleEventAPIResponse:
    event = await EventService(session).create(payload)
    return single_event_response(event)


async def list_events_handler(
    status: Optional[EventStatus] = Query(default=None),
    start_from: Optional[datetime] = Query(default=None),
    start_to: Optional[datetime] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
) -> EventListAPIResponse:
    events, total = await EventService(session).list_all(
        status, start_from, start_to, limit, offset
    )
    return event_list_response(events, total)


async def get_event_handler(
    event_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> SingleEventAPIResponse:
    event = await EventService(session).get(event_id)
    return single_event_response(event)


async def update_event_handler(
    event_id: uuid.UUID,
    payload: EventUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> SingleEventAPIResponse:
    event = await EventService(session).update(event_id, payload)
    return single_event_response(event)


async def delete_event_handler(
    event_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    await EventService(session).delete(event_id)
    return Response(status_code=204)
