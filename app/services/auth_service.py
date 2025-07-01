import secrets

from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.config import get_settings
from app.core.log_config import configure_logger
from app.dtos.activity_status import ActivityStatus
from app.dtos.auth_dto import OauthResponseDto, GoogleAuthUser, TokenData
from app.dtos.user_dto import RegisterUser, UpdateUserProfile
from app.services.jwt_service import JwtService
from app.services.user_service import UserService
from app.utils.constants.constants import AuthConstants
import traceback


settings = get_settings()

class AuthService:
    """Service for user-related operations."""

    def __init__(self, user_service: UserService):
        self.logger = configure_logger(__name__)
        self.user_service: UserService = user_service
        self.oauth = OAuth()
        

        self.oauth.register(
            name='google',
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'}
        )
        

        self.oauth_clients = {}

    def get_oauth_client(self, provider: str):
        if provider not in self.oauth_clients:
            self.oauth_clients[provider] = self.oauth.create_client(provider)
        return self.oauth_clients[provider]

    async def create_oauth_client(self, request: Request, provider: str) -> ActivityStatus:
        self.logger.info(f"received request -> {request} \n Session -> {request.session}", exc_info=True)

        self.logger.info(f"received request to initiate {provider} OAuth login")
        try:
            redirect_url = f"{settings.BACKEND_URL}/api/v1/auth/callback/{provider}"
            
            oauth_state = secrets.token_urlsafe(32)
            request.session['oauth_state'] = oauth_state 
            
            self.logger.info(f"OAuth state generated: {oauth_state}")
            self.logger.info(f"Session key for {provider}: {settings.SESSION_SECRET_KEY}")
            self.logger.info(f"Session registered for {provider}: {request.session}")

            redirect_response = await self.oauth.google.authorize_redirect(request, redirect_uri=redirect_url, prompt="consent", state=oauth_state)
            url_response = redirect_response.headers["location"]
            status_code = redirect_response.status_code
            
            self.logger.info(f"OAuth redirect URL generated: {url_response}")
            self.logger.info(f"State parameter in URL: {oauth_state}")

            return ActivityStatus(code=status_code, message=f"Redirect to {provider} OAuth",
                                  data=OauthResponseDto.from_entity(url_response))
        except Exception as e:
            self.logger.error(f"Error initiating OAuth login for {provider}: {e}", exc_info=True)
            return ActivityStatus(code=500, message="Failed to create OAuth client")

#     async def get_oauth_user(self, request: Request, provider: str, db: AsyncSession) -> RedirectResponse:
#         redirect_url = settings.FRONTEND_URL
        
#         try:
#             self.logger.info(f"Production Debug - Request headers: {dict(request.headers)}")
#             self.logger.info(f"Production Debug - Request cookies: {request.cookies}")
#             self.logger.info(f"Production Debug - Session data: {request.session}")
#             self.logger.info(f"Production Debug - Request URL: {request.url}")
#             self.logger.info(f"Production Debug - Frontend URL: {settings.FRONTEND_URL}")
#             self.logger.info(f"Production Debug - Backend URL: {settings.BACKEND_URL}")
#             self.logger.info(f"Production Debug - Cookie settings: Domain={settings.COOKIE_DOMAIN}, Secure={settings.COOKIE_SECURE}, SameSite={settings.COOKIE_SAMESITE}")
            
#             self.logger.info(f"OAuth client registered for Google {self.oauth}")
#             self.logger.info(f"received request -> {request} \n Session -> {request.session}", exc_info=True)
            
#             self.logger.info(f"OAuth client registered for Google {self.oauth}")
#             self.logger.info(f"received request -> {request} \n Session -> {request.session}", exc_info=True)
           

#             redirect_url_with_token = f"{redirect_url}?access_token={jwt_token}"
#             self.logger.info(f"Redirecting to {redirect_url_with_token} with token")
#             response = RedirectResponse(redirect_url_with_token)
#             self.logger.info(f"Response after redirect: {response}")
#             self.logger.info(f"Received token: {jwt_token}")
#             self.logger.info(f"response: {response}")
#             print(f"response: {response}")
            
#             response.set_cookie(
#                 key=AuthConstants.ACCESS_TOKEN_COOKIE_KEY,
#                 value=jwt_token,
#                 httponly=True,  # Prevents XSS attacks
#                 secure=True,    # Required when same_site="none"
#                 samesite="none", # Note: lowercase in set_cookie
#                 domain=settings.COOKIE_DOMAIN,
#                 max_age=3600
# )
#             self.logger.info(f"Set cookie with key:  and value: {response.__dict__}")
#             self.logger.info(
#                 f"OAuth user successfully retrieved and processed - redirecting to frontend {response.__dict__} headers {response.headers.__dict__}",
#                 exc_info=True)
#             return response
#         except Exception as e:
#             self.logger.error(f"Error during OAuth callback: {e}", exc_info=True)
#             response = RedirectResponse(redirect_url)
#             return response


    async def get_oauth_user(self, request: Request, provider: str, db: AsyncSession) -> RedirectResponse:
        """
        Handle OAuth callback and process user authentication.
        
        Args:
            request: FastAPI Request object
            provider: OAuth provider name (e.g., 'google')
            db: Database session
            
        Returns:
            RedirectResponse with authentication cookie set
        """
        redirect_url = settings.FRONTEND_URL
        
        try:
            # Debug logging for production troubleshooting
            self.logger.info(f"OAuth callback started for provider: {provider}")
            self.logger.info(f"Request URL: {request.url}")
            self.logger.info(f"Request headers: {dict(request.headers)}")
            self.logger.info(f"Request cookies: {request.cookies}")
            self.logger.info(f"Session data: {request.session}")
            
            # Validate OAuth state parameter to prevent CSRF attacks
            received_state = request.query_params.get('state')
            session_state = request.session.get('oauth_state')
            
            self.logger.info(f"Received state: {received_state}, Session state: {session_state}")
            
            # if not received_state or not session_state:
            #     self.logger.error("Missing OAuth state parameter - possible CSRF attack or session issue")
            #     return RedirectResponse(f"{redirect_url}?error=missing_state")
            #
            # if received_state != session_state:
            #     self.logger.error(f"State mismatch - received: {received_state}, expected: {session_state}")
            #     return RedirectResponse(f"{redirect_url}?error=state_mismatch")

            # self.logger.info("OAuth state validation successful")
            
            # Exchange authorization code for access token
            token = await self.oauth.google.authorize_access_token(request)
            
            if not token:
                self.logger.error("No token received from OAuth provider")
                return RedirectResponse(f"{redirect_url}?error=no_token")
                
            if "userinfo" not in token:
                self.logger.error("Token does not contain user information")
                return RedirectResponse(f"{redirect_url}?error=invalid_token")
                
            self.logger.info("OAuth token retrieved successfully")
            
            # Extract user information
            user: GoogleAuthUser = token["userinfo"]
            
            if not user or not hasattr(user, 'email') or not user.email:
                self.logger.error("No valid user information received from OAuth provider")
                return RedirectResponse(f"{redirect_url}?error=no_user_info")
                
            user_email = str(user.email).strip().lower()
            self.logger.info(f"Processing OAuth user: {user_email}")
            
            # Check if user exists and create/update accordingly
            user_exists = await self.user_service.user_exists_by_email(email=user_email)
            self.logger.info(f"User exists check for {user_email}: {user_exists}")
            
            if user_exists:
                # Update existing user profile
                payload = UpdateUserProfile(
                    profile_picture=getattr(user, 'picture', None),
                    first_name=getattr(user, 'given_name', None),
                    last_name=getattr(user, 'family_name', None)
                )
                await self.user_service.update_user_profile(user_email, payload)
                self.logger.info(f"Updated existing user profile for: {user_email}")
            else:
                # Create new user
                payload = RegisterUser(
                    email=user.email,
                    provider=provider,
                    profile_picture=getattr(user, 'picture', None),
                    firstName=getattr(user, 'given_name', None),
                    lastName=getattr(user, 'family_name', None)
                )
                await self.user_service.create_user(payload, db)
                self.logger.info(f"Created new user: {user_email}")
            
            # Generate JWT token
            token_data = TokenData(email=user_email)
            jwt_token = JwtService.generate_token(token_data.__dict__)
            
            if not jwt_token:
                self.logger.error("Failed to generate JWT token")
                return RedirectResponse(f"{redirect_url}?error=token_generation_failed")
                
            self.logger.info(f"Generated JWT token for user: {user_email}")
            
            # Create redirect response
            response = RedirectResponse(redirect_url, status_code=302)
            
            # Set authentication cookie with secure settings
            response.set_cookie(
                key=AuthConstants.ACCESS_TOKEN_COOKIE_KEY,
                value=jwt_token,
                httponly=settings.COOKIE_HTTPONLY,      # Prevents XSS attacks
                secure=settings.COOKIE_SECURE,        # Required for HTTPS and SameSite=None
                samesite="none",    # Allows cross-site requests
            )
            
            # Clean up OAuth state from session
            # request.session.pop('oauth_state', None)
            
            self.logger.info(f"OAuth authentication successful for {user_email}")
            self.logger.info(f"Cookie settings - Domain: {settings.COOKIE_DOMAIN}, Secure: True, SameSite: none")
            self.logger.info(f"Redirecting to: {redirect_url}")
            
            return response

        except Exception as e:
            self.logger.error(f"OAuth callback error: {str(e)}", exc_info=True)
            
            # Return error redirect with specific error information
            error_message = "oauth_error"
            if "state" in str(e).lower():
                error_message = "state_error"
            elif "token" in str(e).lower():
                error_message = "token_error"
            elif "user" in str(e).lower():
                error_message = "user_error"
                
            return RedirectResponse(f"{redirect_url}?error={error_message}")