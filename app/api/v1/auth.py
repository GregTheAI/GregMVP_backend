from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.core.storage.dependencies import get_pg_database
from app.dtos.auth_dto import LoginRequestDto
from app.dtos.user_dto import RegisterUserDto, RegisterUser
from app.services import AuthService, UserService
from app.services.dependencies import get_user_service, get_auth_service
from app.utils.constants.constants import AuthConstants
from app.utils.helpers.api_helpers import api_bad_response, api_created_response, api_response

router = APIRouter(tags=["auth"])

settings = get_settings()
@router.post("/register")
async def register(request: RegisterUserDto, user_service: UserService = Depends(get_user_service), db: AsyncSession = Depends(get_pg_database)) -> JSONResponse:

    create_user_response = await user_service.create_user(RegisterUser(firstName=request.first_name, lastName=request.last_name, password=request.password, email=request.email, provider="direct"), db)
    if create_user_response.isSuccess is False:
        return api_bad_response(create_user_response.message)

    token = create_user_response.data.token

    api_resp = api_created_response(
        data=create_user_response.data,
        message=create_user_response.message)

    api_resp.set_cookie(
                key=AuthConstants.ACCESS_TOKEN_COOKIE_KEY,
                value=token,
                httponly=settings.COOKIE_HTTPONLY,
                secure=True,
                samesite="lax"
            )

    return api_resp


@router.post("/login")
async def login(request: LoginRequestDto, user_service: UserService = Depends(get_user_service)) -> JSONResponse:

    response = await user_service.login(str(request.email), request.password)

    if response.isSuccess is False or response.data is None:
        return api_bad_response(response.message)

    api_resp = api_response(code=response.code, data=response.data, message=response.message)
    api_resp.set_cookie(
                key=AuthConstants.ACCESS_TOKEN_COOKIE_KEY,
                value=response.data.token,
                httponly=settings.COOKIE_HTTPONLY,
                secure=True,
                samesite="lax"
            )
    return api_resp


@router.get("/login/{provider}")
async def login_with_sso(request: Request, provider: str, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.create_oauth_client(request, provider)

@router.get("/callback/{provider}", name="auth_callback")
async def ss0_login_callback(request: Request, provider: str, auth_service: AuthService = Depends(get_auth_service),  db: AsyncSession = Depends(get_pg_database)):
    return await auth_service.get_oauth_user(request, provider, db)
