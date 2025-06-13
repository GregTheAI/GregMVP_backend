from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.dtos.CreateUser import RegisterUserDto
from app.dtos.api_response import ApiResponse
from app.utils.helpers.api_helpers import api_ok_response

router = APIRouter(tags=["auth"])


@router.post("/register")
def register(request: RegisterUserDto)-> JSONResponse:
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
    return { "message": "Password recovery email sent" }


@router.post("/reset-password/")
def reset_password(body: str) :
    return { "message": "Password recovery email sent" }