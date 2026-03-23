import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.events.models import Event


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> Event:
        event = Event(**data)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_by_id(self, event_id: uuid.UUID) -> Optional[Event]:
        return await self.session.get(Event, event_id)

    async def list_all(
        self,
        status: Optional[str] = None,
        start_from: Optional[datetime] = None,
        start_to: Optional[datetime] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Event], int]:
        query = select(Event)
        if status:
            query = query.where(Event.status == status)
        if start_from:
            query = query.where(Event.start_at >= start_from)
        if start_to:
            query = query.where(Event.start_at <= start_to)

        total = await self.session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        result = await self.session.execute(
            query.order_by(Event.start_at.asc()).limit(limit).offset(offset)
        )
        return result.scalars().all(), total

    async def update(self, event: Event, data: dict) -> Event:
        for field, value in data.items():
            setattr(event, field, value)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def delete(self, event: Event) -> None:
        await self.session.delete(event)
        await self.session.commit()
