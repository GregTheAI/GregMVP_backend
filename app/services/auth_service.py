from authlib.integrations.starlette_client import OAuth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.config import settings
from app.core.log_config import configure_logger
from app.dtos.activity_status import ActivityStatus
from app.dtos.auth_dto import OauthResponseDto, GoogleAuthUser, TokenData
from app.dtos.user_dto import RegisterUser, UpdateUserProfile
from app.services.jwt_service import JwtService
from app.services.user_service import UserService
from app.utils.constants.constants import AuthConstants


class AuthService:
    """Service for user-related operations."""

    def __init__(self, user_service: UserService):
        self.logger = configure_logger(__name__)
        self.user_service: UserService = user_service
        self.oauth = OAuth(settings)

        self.oauth.register(
            name='google',
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'}
        )

    async def create_oauth_client(self, request: Request, provider: str) -> ActivityStatus:

        self.logger.info(f"received request to initiate {provider} OAuth login")
        try:
            redirect_url = f"{settings.BACKEND_URL}api/v1/auth/callback/{provider}"
            redirect_response = await self.oauth.create_client(provider).authorize_redirect(request,
                                                                                            redirect_uri=redirect_url,
                                                                                            prompt="consent")

            url_response = redirect_response.headers["location"]
            status_code = redirect_response.status_code
            return ActivityStatus(code=status_code, message=f"Redirect to {provider} OAuth",
                                  data=OauthResponseDto.from_entity(url_response))
        except Exception as e:
            self.logger.error(f"Error initiating OAuth login for {provider}: {e}", exc_info=True)
            return ActivityStatus(code=500, message="Failed to create OAuth client")


    async def get_oauth_user(self, request: Request, provider: str, db: AsyncSession) -> RedirectResponse:
        redirect_url = settings.FRONTEND_URL
        try:
            token = await self.oauth.create_client(provider).authorize_access_token(request)
            user: GoogleAuthUser = token["userinfo"]

            if user is None:
                return RedirectResponse(redirect_url)

            user_email = str(user.email)

            user_exists = await self.user_service.user_exists_by_email(email=user_email)

            self.logger.info(f"User exists: {user_exists} for email: {user_email}")
            if user_exists:
                payload = UpdateUserProfile(profile_picture=user.picture, first_name=user.given_name, last_name=user.family_name)
                await self.user_service.update_user_profile(user_email, payload)
            else:
                payload = RegisterUser(email=user.email, provider=provider, profile_picture=user.picture,
                                       firstName=user.given_name, lastName=user.family_name)
                await self.user_service.create_user(payload, db)

            token_data = TokenData(email= user_email)
            jwt_token = JwtService.generate_token(token_data.__dict__)
            response = RedirectResponse(redirect_url)
            response.set_cookie(
                key=AuthConstants.ACCESS_TOKEN_COOKIE_KEY,
                value=jwt_token,
                httponly=settings.COOKIE_HTTPONLY,
                secure=True,
                samesite="lax"
            )
            self.logger.info("OAuth user successfully retrieved and processed.")
            return response
        except Exception as e:
            self.logger.error(f"Error during OAuth callback: {e}", exc_info=True)
            return RedirectResponse(redirect_url)
