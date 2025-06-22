from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.dtos.user_dto import UserResponseDto
from app.middlewares.authenticate import get_current_user
from app.utils.helpers.api_helpers import api_response, api_not_found

router = APIRouter(tags=["users"])

@router.get("/me")
async def get_user_profile(user: UserResponseDto = Depends(get_current_user)) -> JSONResponse:
    if user is None:
        return api_not_found(message="User not found")

    return api_response(code=200, data=user, message="Success")


@router.put("/{user_id}")
def update_user_profile(user_id: str):
    return api_response(code=200, data=user_id, message="Success")
