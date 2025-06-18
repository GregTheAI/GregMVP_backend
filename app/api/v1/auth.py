from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.core.storage.dependencies import get_pg_database
from app.dtos.auth_dto import LoginRequestDto
from app.dtos.user_dto import RegisterUserDto, RegisterUser
from app.services import AuthService, UserService
from app.services.dependencies import get_user_service, get_auth_service
from app.utils.helpers.api_helpers import api_bad_response, api_created_response, api_response

router = APIRouter(tags=["auth"])

@router.post("/register")
async def register(request: RegisterUserDto, user_service: UserService = Depends(get_user_service), db: AsyncSession = Depends(get_pg_database)) -> JSONResponse:

    create_user_response = await user_service.create_user(RegisterUser(firstName=request.first_name, lastName=request.last_name, password=request.password, email=request.email, provider="direct"), db)
    if create_user_response.isSuccess is False:
        return api_bad_response(create_user_response.message)

    return api_created_response(
        data=create_user_response.data,
        message=create_user_response.message)


@router.post("/login")
async def login(request: LoginRequestDto, user_service: UserService = Depends(get_user_service)):

    response = await user_service.login(str(request.email), request.password)
    return api_response(code=response.code, data=response.data, message=response.message)


@router.get("/login/{provider}")
async def login_with_sso(request: Request, provider: str, auth_service: AuthService = Depends(get_auth_service)) -> JSONResponse:
    response = await auth_service.create_oauth_client(request, provider)
    return api_response(code=response.code, data=response.data, message=response.message)

@router.get("/callback/{provider}")
async def ss0_login_callback(request: Request, provider: str, auth_service: AuthService = Depends(get_auth_service),  db: AsyncSession = Depends(get_pg_database)):
    return await auth_service.get_oauth_user(request, provider, db)
