from fastapi import APIRouter

from app.api.events.schemas import EventListAPIResponse, SingleEventAPIResponse
from app.api.events.views import (
    create_event_handler,
    delete_event_handler,
    get_event_handler,
    list_events_handler,
    update_event_handler,
)

router = APIRouter(prefix="/events", tags=["Events"])

router.add_api_route(
    "",
    create_event_handler,
    methods=["POST"],
    response_model=SingleEventAPIResponse,
    status_code=201,
)
router.add_api_route(
    "", list_events_handler, methods=["GET"], response_model=EventListAPIResponse
)
router.add_api_route(
    "/{event_id}",
    get_event_handler,
    methods=["GET"],
    response_model=SingleEventAPIResponse,
)
router.add_api_route(
    "/{event_id}",
    update_event_handler,
    methods=["PATCH"],
    response_model=SingleEventAPIResponse,
)
router.add_api_route(
    "/{event_id}", delete_event_handler, methods=["DELETE"], status_code=204
)
