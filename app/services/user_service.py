
from fastapi import Depends

from app.dtos.activity_status import ActivityStatus
from app.dtos.user_dto import UserResponseDto, RegisterUserDto, RegisterUser, UpdateUserProfile
from app.entities import User
from app.repositories.role_repository import RoleRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository
from app.services.jwt_service import JwtService


class UserService:
    """Service for user-related operations."""

    def __init__(self, user_repo=Depends(UserRepository), subscription_repo=Depends(SubscriptionRepository),
                 role_repo=Depends(RoleRepository)):
        self.user_repo: UserRepository = user_repo
        self.subscription_repo: SubscriptionRepository = subscription_repo
        self.role_repo: RoleRepository = role_repo

    async def create_user(self, user: RegisterUser) -> ActivityStatus:
        """Create a new user in the database."""
        try:
            email_str = str(user.email)
            existing_user = await self.user_repo.get_user_by_email(email=email_str)
            if existing_user:
                return ActivityStatus(code=400, message="Email already registered")

            # standard_user - role for the user
            # get subscription by name from the db
            free_plan = await self.subscription_repo.get_subscription_by_name("free")
            if free_plan is None:
                return ActivityStatus(code=404, message="Free subscription plan not found")

            free_plan_id = free_plan.id

            user_role = await self.role_repo.get_role_by_name("standard_user")

            if user_role is None:
                return ActivityStatus(code=404, message="Standard user role not found")

            user_role_id = user_role.id
            # username should extract from email text before @
            username = email_str.split('@')[0]
            if user.password is not None:
                user.password = JwtService.hash_password(user.password)

            is_email_verified = False
            if user.provider != "direct":
                # If the user is registering through an OAuth provider, we don't need a password
                is_email_verified = True

            request = User(
                email=user.email,
                password=user.password,
                username=username,
                role_id=user_role_id,
                subscription_id=free_plan_id,
                provider=user.provider,
                profile_picture=user.profile_picture,
                full_name=user.name,
                is_email_verified=is_email_verified
            )
            created_user = await self.user_repo.create_user(request)
            return ActivityStatus(code=200, message="User created successfully", data=UserResponseDto.from_entity(created_user))
        except Exception as e:
            return ActivityStatus(code=500, message="Failed to create user")

    async def get_user_by_email(self, email: str) -> UserResponseDto | None:
        """Create a new user in the database."""
        user = await self.user_repo.get_user_by_email(email=email)
        if user is None:
            return None
        return UserResponseDto.from_entity(user)

    async def user_exists_by_email(self, email: str) -> bool:
       return await self.user_repo.user_exists_by_email(email=email)

    async def update_user_profile(self, email: str, user: UpdateUserProfile) -> ActivityStatus:
        existing_user = await self.user_repo.get_user_by_email(email=email)
        if existing_user is None:
            return ActivityStatus(code=404, message="User not found")

        existing_user.profile_picture = user.profile_picture
        existing_user.full_name = user.name

        updated_user = await self.user_repo.update_user_profile(existing_user)
        return ActivityStatus(code=200, message="User created successfully",
                              data=UserResponseDto.from_entity(updated_user))