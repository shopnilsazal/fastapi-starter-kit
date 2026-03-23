from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from app.api.v1.users.schemas import UserResponse
from app.api.v1.users.views import (
    create_user,
    deactivate_user,
    get_user,
    list_users,
    update_user,
)

router = APIRouter(prefix="/users", tags=["Users"])

router.add_api_route(
    "/",
    create_user,
    methods=["POST"],
    status_code=HTTP_201_CREATED,
    response_model=UserResponse,
)
router.add_api_route(
    "/", list_users, methods=["GET"], response_model=list[UserResponse]
)
router.add_api_route(
    "/{user_id}", get_user, methods=["GET"], response_model=UserResponse
)
router.add_api_route(
    "/{user_id}", update_user, methods=["PATCH"], response_model=UserResponse
)
router.add_api_route(
    "/{user_id}", deactivate_user, methods=["DELETE"], response_model=UserResponse
)
