from fastapi import Depends

from app.repositories.role_repository import RoleRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_subscription_repository import UserSubscriptionRepository
from app.services import UserService, AuthService
from app.services.s3_service import S3Service
from app.services.extractor import ExtractorService


def get_user_service(
        user_repo: UserRepository = Depends(),
        subscription_repo: SubscriptionRepository = Depends(),
        role_repo: RoleRepository = Depends(),
        user_sub_repo: UserSubscriptionRepository = Depends(),
) -> UserService:
    return UserService(user_repo, subscription_repo, role_repo, user_sub_repo)


def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service)

def get_s3_service() -> S3Service:
    return S3Service()

def get_extractor_service() -> ExtractorService:
    return ExtractorService()