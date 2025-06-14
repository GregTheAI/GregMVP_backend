from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from app.dtos.user_dto import RegisterUserDto
from app.services import AuthService, UserService
from app.services.dependencies import get_user_service
from app.utils.helpers.api_helpers import api_ok_response, api_bad_response, api_created_response

router = APIRouter(tags=["auth"])

@router.post("/register")
async def register(request: RegisterUserDto, user_repo: UserService = Depends(get_user_service)) -> JSONResponse:
    create_user_response = await user_repo.create_user(request)
    if create_user_response.isSuccess is False:
        return api_bad_response(create_user_response.message)

    return api_created_response(
        data=create_user_response.data,
        message=create_user_response.message)


@router.post("/login")
def login(request, user_repo: UserService = Depends(get_user_service)):

    return {
        "access_token": "fake-token"}


@router.post("/password-recovery/{email}")
def recover_password(email: str):
    return {"message": "Password recovery email sent"}


@router.post("/reset-password/")
def reset_password(body: str):
    return {"message": "Password recovery email sent"}
