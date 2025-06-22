from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.activity_status import ActivityStatus
from app.dtos.auth_dto import TokenData, LoginResponseDto
from app.dtos.user_dto import UserResponseDto, RegisterUser, UpdateUserProfile
from app.entities import User, UserSubscription
from app.repositories.role_repository import RoleRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_subscription_repository import UserSubscriptionRepository
from app.services.jwt_service import JwtService


class UserService:
    """Service for user-related operations."""

    def __init__(self, user_repo=Depends(UserRepository), subscription_repo=Depends(SubscriptionRepository),
                 role_repo=Depends(RoleRepository),
                 user_subscription_repo: UserSubscriptionRepository = Depends(UserSubscriptionRepository)):
        self.user_repo: UserRepository = user_repo
        self.subscription_repo: SubscriptionRepository = subscription_repo
        self.role_repo: RoleRepository = role_repo
        self.user_subscription_repo: UserSubscriptionRepository = user_subscription_repo

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

            return ActivityStatus(code=200, message="User created successfully",
                                  data=UserResponseDto(id=str(created_user.id), firstName=created_user.first_name,
                                                       lastName=created_user.last_name, email=str(created_user.email),
                                                       profilePicture=created_user.profile_picture,
                                                       isEmailVerified=created_user.is_email_verified,
                                                       username=created_user.username))
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
        user = await self.user_repo.get_user_by_email(email=email)
        if user is None:
            return ActivityStatus(code=404, message="No account found")

        if not user.is_active:
            return ActivityStatus(code=403, message="Account is inactive")

        if not JwtService.verify_password(password, db_password=user.password):
            return ActivityStatus(code=401, message="Invalid credentials")

        token_data = TokenData(
            email=str(user.email)
        )
        jwt_token = JwtService.generate_token(token_data.__dict__)

        return ActivityStatus(code=200, message="Login successful", data=LoginResponseDto.from_entity(user, jwt_token))

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
