from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from app.dtos.user_dto import RegisterUserDto
from app.services import AuthService, UserService
from app.utils.helpers.api_helpers import api_ok_response, api_bad_response

router = APIRouter(tags=["auth"])


@router.post("/user")
async def get_user(request: RegisterUserDto, user_repo: UserService = Depends()) -> JSONResponse:

    user = await user_repo.get_user_by_email(email=str(request.email))
    if user is None:
        return api_bad_response("User not found", errors={"email": "User with this email does not exist"})

    return api_ok_response(
        data=user,
        message="User registered successfully")


@router.post("/register")
def register(request: RegisterUserDto, user_repo: AuthService = Depends()) -> JSONResponse:
    return api_ok_response(
        data=request,
        message="User registered successfully"
    )


@router.post("/login")
def login():
    return {
        "access_token": "fake-token"}


@router.post("/password-recovery/{email}")
def recover_password(email: str):
    return {"message": "Password recovery email sent"}


@router.post("/reset-password/")
def reset_password(body: str):
    return {"message": "Password recovery email sent"}
