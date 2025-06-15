from fastapi import APIRouter, Request
from fastapi.params import Depends
from starlette.responses import JSONResponse

from app.dtos.user_dto import RegisterUserDto, RegisterUser
from app.services import AuthService, UserService
from app.services.dependencies import get_user_service, get_auth_service
from app.utils.helpers.api_helpers import api_bad_response, api_created_response, api_ok_response

router = APIRouter(tags=["auth"])

@router.post("/register")
async def register(request: RegisterUserDto, user_service: UserService = Depends(get_user_service)) -> JSONResponse:

    create_user_response = await user_service.create_user(RegisterUser(password=request.password, email=request.email, provider="direct"))
    if create_user_response.isSuccess is False:
        return api_bad_response(create_user_response.message)

    return api_created_response(
        data=create_user_response.data,
        message=create_user_response.message)


@router.post("/login")
def login(request, user_repo: UserService = Depends(get_user_service)):

    return {
        "access_token": "fake-token"}

@router.get("/login/{provider}")
async def login_with_sso(request: Request, provider: str, auth_service: AuthService = Depends(get_auth_service)) -> JSONResponse:
    response = await auth_service.create_oauth_client(request, provider)
    return api_ok_response(data=response.data, message=response.message)

@router.get("/callback/{provider}")
async def ss0_login_callback(request: Request, provider: str, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.get_oauth_user(request, provider)


@router.post("/password-recovery/{email}")
def recover_password(email: str):
    return {"message": "Password recovery email sent"}


@router.post("/reset-password/")
def reset_password(body: str):
    return {"message": "Password recovery email sent"}
