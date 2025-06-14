from fastapi import Depends

from app.repositories.role_repository import RoleRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository
from app.services import UserService


def get_user_service(
    user_repo: UserRepository = Depends(),
    subscription_repo: SubscriptionRepository = Depends(),
    role_repo: RoleRepository = Depends(),
) -> UserService:
    return UserService(user_repo, subscription_repo, role_repo)