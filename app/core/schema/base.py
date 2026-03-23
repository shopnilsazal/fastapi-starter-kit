from typing import Optional

from pydantic import field_validator

from app.core.schema import PydanticModel


class BaseResponse(PydanticModel):
    success: bool
    code: int


class LogData(PydanticModel):
    request_id: Optional[str] = None
    user_host: Optional[str] = None
    user_agent: Optional[str] = None
    path: Optional[str] = None
    method: Optional[str] = None
    path_params: Optional[dict] = None
    query_params: Optional[dict] = None
    payload: Optional[dict] = None
    request_data: Optional[str] = None
    response_data: Optional[str] = None
    response_code: Optional[int] = None
    response_time: Optional[float] = None

    class Config:
        validate_assignment = True

    @field_validator("request_data", mode="before")
    def prepare_request_data(cls, v, values):
        res = dict()
        if "path_params" in values and values["path_params"]:
            res["path_params"] = values["path_params"]
        if "query_params" in values and values["query_params"]:
            res["query_params"] = values["query_params"]
        if "payload" in values and values["payload"]:
            res["payload"] = values["payload"]
        return res or None
