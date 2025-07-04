from datetime import datetime, timedelta

from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.log_config import configure_logger
from app.dtos.activity_status import ActivityStatus
from app.dtos.auth_dto import TokenData, LoginResponseDto, ResetPasswordDto
from app.dtos.user_dto import UserResponseDto, RegisterUser, UpdateUserProfile, VerifyEmailDto
from app.entities import User, UserSubscription
from app.repositories.role_repository import RoleRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_subscription_repository import UserSubscriptionRepository
from app.services.email_service import EmailService
from app.services.jwt_service import JwtService
from app.utils.helpers.email.wait_list import send_email_confirmation_html, forgot_password_html
from app.utils.helpers.utils import generate_otp_code

settings = get_settings()

class UserService:
    """Service for user-related operations."""

    def __init__(self, user_repo=Depends(UserRepository), subscription_repo=Depends(SubscriptionRepository),
                 role_repo=Depends(RoleRepository),
                 user_subscription_repo: UserSubscriptionRepository = Depends(UserSubscriptionRepository), email_service=Depends(EmailService)):
        self.logger = configure_logger(__name__)
        self.user_repo: UserRepository = user_repo
        self.subscription_repo: SubscriptionRepository = subscription_repo
        self.role_repo: RoleRepository = role_repo
        self.user_subscription_repo: UserSubscriptionRepository = user_subscription_repo
        self.email_service : EmailService = email_service

    @staticmethod
    async def _generate_token(email, expiration_minutes: float | None = None) -> str:
        token_data = TokenData(email=str(email))
        jwt_token = JwtService.generate_token(token_data.__dict__, expiration_minutes)
        return jwt_token

    async def create_user(self, user: RegisterUser, db: AsyncSession) -> ActivityStatus:
        """Create a new user in the database."""
        try:
            email_str = str(user.email)
            existing_user = await self.user_repo.get_user_by_email(email=email_str)
            if existing_user:
                return ActivityStatus(code=400, message="Email already registered")

            free_plan = await self.subscription_repo.get_subscription_by_name("free")
            if free_plan is None:
                return ActivityStatus(code=404, message="Free subscription plan not found")

            free_plan_id = free_plan.id

            user_role = await self.role_repo.get_role_by_name("standard_user")
            if user_role is None:
                return ActivityStatus(code=404, message="Standard user role not found")

            user_role_id = user_role.id
            username = email_str.split('@')[0]
            if user.password is not None:
                user.password = JwtService.hash_password(user.password)

            is_email_verified = False
            if user.provider != "direct":
                is_email_verified = True

            request = User(
                email=user.email,
                password=user.password,
                username=username,
                role_id=user_role_id,
                subscription_id=free_plan_id,
                provider=user.provider,
                profile_picture=user.profile_picture,
                first_name=user.first_name,
                last_name=user.last_name,
                is_email_verified=is_email_verified
            )
            created_user = await self.user_repo.create_user(request)
            if created_user is None:
                await db.rollback()
                return ActivityStatus(code=424, message="Failed to create user")

            start_date = datetime.utcnow()
            end_date = start_date + timedelta(days=29)
            user_subscription_payload = UserSubscription(
                user_id=created_user.id,
                subscription_id=free_plan_id,
                start_date=start_date,
                end_date=end_date
            )

            created_user_subscription = await self.user_subscription_repo.create_user_subscription(
                user_subscription_payload)
            if created_user_subscription is None:
                await db.rollback()
                return ActivityStatus(code=424, message="Failed to setup user subscription")

            jwt_token = await self._generate_token(created_user.email)

            user_data= UserResponseDto(id=str(created_user.id), firstName=created_user.first_name,
                                                       lastName=created_user.last_name, email=str(created_user.email),
                                                       profilePicture=created_user.profile_picture,
                                                       isEmailVerified=created_user.is_email_verified,
                                                       username=created_user.username, token=jwt_token)

            await self.send_user_email_verification_email(user_data)

            return ActivityStatus(code=201, message="User created successfully",
                                  data=user_data)
        except Exception as e:
            await db.rollback()
            return ActivityStatus(code=500, message="Failed to create user")

    async def get_user_by_email(self, email: str) -> UserResponseDto | None:
        """Create a new user in the database."""
        user = await self.user_repo.get_user_by_email(email=email)
        if user is None:
            return None
        return UserResponseDto(id=str(user.id), email=str(user.email), firstName=user.first_name,
                               lastName=user.last_name, profilePicture=user.profile_picture,
                               isEmailVerified=user.is_email_verified, username=user.username)


    async def user_exists_by_email(self, email: str) -> bool:
        return await self.user_repo.user_exists_by_email(email=email)

    async def login(self, email: str, password: str) -> ActivityStatus[LoginResponseDto]:
        """Login user by email and password."""
        try:
            self.logger.info("Attempting to login user with email: %s", email)
            user = await self.user_repo.get_user_by_email(email=email)
            if user is None:
                return ActivityStatus(code=404, message="No account found")

            if not user.is_active:
                return ActivityStatus(code=403, message="Account is inactive")

            if not JwtService.verify_password(password, db_password=user.password):
                return ActivityStatus(code=401, message="Invalid credentials")

            jwt_token = await self._generate_token(email)

            return ActivityStatus(code=200, message="Login successful",
                                  data=LoginResponseDto.from_entity(user, jwt_token))
        except Exception as e:
            self.logger.error(f"Failed to login user: {e}", exc_info=True)
            return ActivityStatus(code=500, message="Failed to login user", data=None)

    async def update_user_profile(self, email: str, user: UpdateUserProfile) -> ActivityStatus[UserResponseDto]:
        existing_user = await self.user_repo.get_user_by_email(email=email)
        if existing_user is None:
            return ActivityStatus(code=404, message="User not found")

        existing_user.profile_picture = user.profile_picture
        existing_user.first_name = user.first_name
        existing_user.last_name = user.last_name

        updated_user = await self.user_repo.update_user_profile(existing_user)
        return ActivityStatus(code=200, message="User created successfully",
                              data=UserResponseDto(id=str(updated_user.id), firstName=updated_user.first_name,
                                                       lastName=updated_user.last_name, email=str(updated_user.email),
                                                       profilePicture=updated_user.profile_picture,
                                                       isEmailVerified=updated_user.is_email_verified,
                                                       username=updated_user.username))

    async def send_user_email_verification_email(self, user: UserResponseDto) -> ActivityStatus[VerifyEmailDto]:

        """Send email verification to the user."""
        email = user.email
        name = user.first_name
        jwt_token = await self._generate_token(email, 5)

        email = email.strip()
        verification_url = f"{settings.FRONTEND_EMAIL_VERIFICATION_URL}?token={jwt_token}"

        html_content = send_email_confirmation_html(name, verification_url)
        self.email_service.send_email_background(to_email=email,
                                                 subject="Email verification",
                                                 html_content=html_content)

        return ActivityStatus(code=200, message="Email sent successfully",
                              data=VerifyEmailDto(email=email))

    async def update_user_email_verification_status(self, email: str) -> ActivityStatus[UserResponseDto]:
        """Update the email verification status of a user."""
        self.logger.info("Attempting to update user email verification status for email: %s", email)

        existing_user = await self.user_repo.get_user_by_email(email=email)

        if existing_user is None:
            return ActivityStatus(code=404, message="User not found")

        if existing_user.is_email_verified:
            return ActivityStatus(code=400, message="Email is already verified")

        existing_user.is_email_verified = True

        updated_user = await self.user_repo.update_user_profile(existing_user)
        return ActivityStatus(code=200, message="Email verified successfully",
                              data=UserResponseDto(id=str(updated_user.id), firstName=updated_user.first_name,
                                                   lastName=updated_user.last_name, email=str(updated_user.email),
                                                   profilePicture=updated_user.profile_picture,
                                                   isEmailVerified=updated_user.is_email_verified,
                                                   username=updated_user.username))

    async def forgot_password(self, email: str) -> ActivityStatus[UserResponseDto]:
        self.logger.info("Attempting to reset password for email: %s", email)

        existing_user = await self.user_repo.get_user_by_email(email=email)

        if existing_user is None:
            return ActivityStatus(code=404, message="User not found")

        if existing_user.is_active is False:
            return ActivityStatus(code=400, message="Account is inactive")

        otp = generate_otp_code(4)

        existing_user.reset_password_email_token = JwtService.hash_password(otp)
        existing_user.resetPasswordExpirationTime = datetime.utcnow() + timedelta(minutes=5)

        updated_user = await self.user_repo.update_user_profile(existing_user)

        if updated_user is None:
            return ActivityStatus(code=424, message="Failed to send OTP")

        email = email.strip()
        verification_url = f"{settings.FRONTEND_FORGOT_PASSWORD_URL}?token={otp}"
        html_content = forgot_password_html(existing_user.first_name, verification_url, otp)
        self.email_service.send_email_background(to_email=email,
                                                 subject="Forgot Password",
                                                 html_content=html_content)

        return ActivityStatus(code=200, message="Forgot password email sent successfully",
                              data=UserResponseDto(id=str(updated_user.id), firstName=updated_user.first_name,
                                                   lastName=updated_user.last_name, email=str(updated_user.email),
                                                   profilePicture=updated_user.profile_picture,
                                                   isEmailVerified=updated_user.is_email_verified,
                                                   username=updated_user.username))

    async def reset_password(self, request: ResetPasswordDto) -> ActivityStatus[UserResponseDto]:
        """Reset the password for a user."""
        existing_user = await self.user_repo.get_user_by_email(email=str(request.email))

        if existing_user is None:
            return ActivityStatus(code=404, message="User not found")

        if existing_user.is_active is False:
            return ActivityStatus(code=400, message="Account is inactive")

        if existing_user.reset_password_email_token is None or existing_user.resetPasswordExpirationTime is None:
            return ActivityStatus(code=400, message="Reset password token is not set or expired")

        if existing_user.resetPasswordExpirationTime < datetime.utcnow():
            existing_user.reset_password_email_token = None
            existing_user.resetPasswordExpirationTime = None
            await self.user_repo.update_user_profile(existing_user)
            return ActivityStatus(code=400, message="Reset password token has expired")

        if JwtService.verify_password(request.token, existing_user.reset_password_email_token) is False:
            return ActivityStatus(code=400, message="Invalid reset password token")

        existing_user.password = JwtService.hash_password(request.password)
        existing_user.reset_password_email_token = None
        existing_user.resetPasswordExpirationTime = None
        updated_user = await self.user_repo.update_user_profile(existing_user)
        if updated_user is None:
            return ActivityStatus(code=424, message="Failed to reset password")

        self.logger.info("Password reset successfully for email: %s", request.email)

        return ActivityStatus(code=200, message="Password reset successfully",
                              data=UserResponseDto(id=str(updated_user.id), firstName=updated_user.first_name,
                                                   lastName=updated_user.last_name, email=str(updated_user.email),
                                                   profilePicture=updated_user.profile_picture,
                                                   isEmailVerified=updated_user.is_email_verified,
                                                   username=updated_user.username))
