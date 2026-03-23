import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from app.api.v1.events.models import Event
from app.api.v1.events.repositories import EventRepository
from app.api.v1.events.schemas import EventCreateRequest, EventUpdateRequest
from app.core.errors.api_exception import APIException


class EventService:
    def __init__(self, session: AsyncSession):
        self.repo = EventRepository(session)

    async def create(self, payload: EventCreateRequest) -> Event:
        return await self.repo.create(payload.model_dump())

    async def get(self, event_id: uuid.UUID) -> Event:
        event = await self.repo.get_by_id(event_id)
        if not event:
            raise APIException(
                msg="Event not found", code=40401, http_code=HTTP_404_NOT_FOUND
            )
        return event

    async def list_all(
        self,
        status: Optional[str] = None,
        start_from: Optional[datetime] = None,
        start_to: Optional[datetime] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Event], int]:
        return await self.repo.list_all(status, start_from, start_to, limit, offset)

    async def update(self, event_id: uuid.UUID, payload: EventUpdateRequest) -> Event:
        event = await self.get(event_id)
        return await self.repo.update(event, payload.model_dump(exclude_unset=True))

    async def delete(self, event_id: uuid.UUID) -> None:
        event = await self.get(event_id)
        await self.repo.delete(event)
