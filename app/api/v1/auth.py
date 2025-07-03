from authlib.integrations.starlette_client import OAuth
from authlib.oauth2.rfc6749 import OAuth2Token
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse

from app.core.config import get_settings
from app.core.storage.dependencies import get_pg_database
from app.dtos.api_response import ApiResponse
from app.dtos.auth_dto import LoginRequestDto, TokenData
from app.dtos.user_dto import RegisterUserDto, RegisterUser, UpdateUserProfile, UserResponseDto, VerifyEmailDto
from app.middlewares.authenticate import get_current_user
from app.services import UserService
from app.services.dependencies import get_user_service
from app.services.jwt_service import JwtService
from app.utils.constants.constants import AuthConstants
from app.utils.helpers.api_helpers import api_bad_response, api_created_response, api_response

router = APIRouter(tags=["auth"])

settings = get_settings()

oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
@router.post("/register")
async def register(request: RegisterUserDto, user_service: UserService = Depends(get_user_service), db: AsyncSession = Depends(get_pg_database)) -> JSONResponse:

    create_user_response = await user_service.create_user(RegisterUser(firstName=request.first_name, lastName=request.last_name, password=request.password, email=request.email, provider="direct"), db)
    if create_user_response.isSuccess is False:
        return api_response(code=create_user_response.code, message=create_user_response.message, data=create_user_response.data)

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
async def login_with_sso(request: Request, provider: str):
    redirect_url = f"{settings.BACKEND_URL}/api/v1/auth/callback/{provider}"
    return await oauth.google.authorize_redirect(request, redirect_uri=redirect_url, prompt="consent")

@router.get("/callback/{provider}")
async def ss0_login_callback(request: Request, provider: str, user_service: UserService = Depends(get_user_service), db: AsyncSession = Depends(get_pg_database)) -> RedirectResponse:
    try:
        user_response: OAuth2Token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        return RedirectResponse(f"{settings.FRONTEND_URL}?error=unauthorized")

    user_info = user_response.get("userinfo")

    user_email = str(user_info.email).strip().lower()

    user_exists = await user_service.user_exists_by_email(email=user_email)

    if user_exists:
        # Update existing user profile
        payload = UpdateUserProfile(
            profile_picture=getattr(user_info, 'picture', None),
            first_name=getattr(user_info, 'given_name', None),
            last_name=getattr(user_info, 'family_name', None)
        )
        await user_service.update_user_profile(user_email, payload)
    else:
        # Create new user
        payload = RegisterUser(
            email=user_info.email,
            provider=provider,
            profile_picture=getattr(user_info, 'picture', None),
            firstName=getattr(user_info, 'given_name', None),
            lastName=getattr(user_info, 'family_name', None)
        )
        await user_service.create_user(payload, db)

    token_data = TokenData(email=user_email)
    jwt_token = JwtService.generate_token(token_data.__dict__)

    if not jwt_token:
        return RedirectResponse(f"{settings.FRONTEND_URL}?error=token_generation_failed")
    response = RedirectResponse(settings.FRONTEND_URL)

    response.set_cookie(
        key=AuthConstants.ACCESS_TOKEN_COOKIE_KEY,
        value=jwt_token,
        httponly=settings.COOKIE_HTTPONLY,  # Prevents XSS attacks
        secure=settings.COOKIE_SECURE,  # Required for HTTPS and SameSite=None
        samesite="none",  # Allows cross-site requests
    )

    return response


# @router.get("/login/{provider}")
# async def login_with_sso(request: Request, provider: str, auth_service: AuthService = Depends(get_auth_service)):
#     return await auth_service.create_oauth_client(request, provider)
#
# @router.get("/callback/{provider}", name="auth_callback")
# async def ss0_login_callback(request: Request, provider: str, auth_service: AuthService = Depends(get_auth_service),  db: AsyncSession = Depends(get_pg_database)):
#     return await auth_service.get_oauth_user(request, provider, db)

@router.post("/verify-email", response_model=ApiResponse[VerifyEmailDto])
async def manual_verify_email(user: UserResponseDto = Depends(get_current_user), user_service: UserService = Depends(get_user_service)) -> JSONResponse:

    if user.is_email_verified:
        return api_bad_response(message="Email is already verified")

    response = await user_service.send_user_email_verification_email(user)

    if response.isSuccess is False or response.data is None:
        return api_bad_response(response.message)

    api_resp = api_response(code=response.code, data=response.data, message=response.message)
    return api_resp


@router.get("/verify-email", response_model=ApiResponse[UserResponseDto])
async def verify_email(user: UserResponseDto = Depends(get_current_user), user_service: UserService = Depends(get_user_service)) -> JSONResponse:

    response = await user_service.update_user_email_verification_status(user.email)

    api_resp = api_response(code=response.code, data=response.data, message=response.message)
    return api_resp
