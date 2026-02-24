from typing import Any, Optional

from app.core.schema import PydanticModel

from .base import BaseResponse


class ErrorDataSchema(PydanticModel):
    error_message: str = "Internal Server Error"
    details: Any | None = None


class ErrorResponseSchema(BaseResponse):
    success: bool = False
    code: int = 50001
    data: ErrorDataSchema | None = None
