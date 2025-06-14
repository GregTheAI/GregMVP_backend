from fastapi import HTTPException, Depends

from app.dtos.user_dto import UserResponseDto, RegisterUserDto
from app.entities import User
from app.repositories.user_repository import UserRepository
from app.services.jwt_service import JwtService

class UserService:
    """Service for user-related operations."""
    def __init__(self, user_repo = Depends(UserRepository)):
        self.user_repo = user_repo

    async def create_user(self, user: RegisterUserDto) -> UserResponseDto:
        """Create a new user in the database."""
        existing_user = await self.user_repo.get_user_by_email(email=user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = JwtService.hash_password(user.password)
        # standard_user - role for the user
        # free_plan = subscription plan for the user
        # username should extract from email text before @
        request = User(
            email=user.email,
            password=hashed_password,
            username=user.username,
        )
        created_user = await self.user_repo.create_user(user)
        return UserResponseDto(created_user)

    async def get_user_by_email(self, email: str) -> UserResponseDto | None:
        """Create a new user in the database."""
        user = await self.user_repo.get_user_by_email(email=email)
        if user is None:
            return None
        return UserResponseDto(user)
