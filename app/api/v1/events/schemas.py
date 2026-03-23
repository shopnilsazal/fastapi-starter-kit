import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import ConfigDict, Field, model_validator

from app.core.schema import PydanticModel
from app.core.schema.base import BaseResponse


class EventStatus(str, Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    completed = "completed"


class EventCreateRequest(PydanticModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = None
    start_at: datetime
    end_at: Optional[datetime] = None
    is_all_day: bool = False
    status: EventStatus = EventStatus.scheduled

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_at and self.end_at <= self.start_at:
            raise ValueError("end_at must be after start_at")
        return self


class EventUpdateRequest(PydanticModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    is_all_day: Optional[bool] = None
    status: Optional[EventStatus] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_at and self.end_at and self.end_at <= self.start_at:
            raise ValueError("end_at must be after start_at")
        return self


class EventResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: Optional[str]
    location: Optional[str]
    start_at: datetime
    end_at: Optional[datetime]
    is_all_day: bool
    status: str
    created_at: datetime
    updated_at: Optional[datetime]


class EventListResponse(PydanticModel):
    items: list[EventResponse]
    total: int


class SingleEventAPIResponse(BaseResponse):
    success: bool = True
    code: int = 200
    data: EventResponse


class EventListAPIResponse(BaseResponse):
    success: bool = True
    code: int = 200
    data: EventListResponse
