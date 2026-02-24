import time

from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.logging import logger
from app.core.schema.base import LogData

from .utils import get_matching_route_path, get_path_params


class LoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        start_time = time.perf_counter()
        request = Request(scope)
        path: str = get_matching_route_path(request)
        path_params: dict = get_path_params(request)
        log_data = LogData(
            request_id=request.state.request_id,
            user_host=request.client.host,
            user_agent=request.headers.get("User-Agent", ""),
            path=path,
            method=request.method,
            path_params=path_params,
            query_params=request.query_params.__dict__["_dict"],
            payload=dict(),
        )
        request.state.log_data = log_data
        logger.info("Request Received", extra=log_data.model_dump())
        try:
            async def send_with_response(message):
                if message["type"] == "http.response.start":
                    log_data.response_code = message["status"]
                await send(message)

            await self.app(scope, receive, send_with_response)
        except Exception as e:
            log_data.response_code = 500
            logger.error(str(e), extra=log_data.model_dump())
            raise
        finally:
            end_time = time.perf_counter()
            log_data.response_time = end_time - start_time
            logger.info("Response Sent", extra=log_data.model_dump())
