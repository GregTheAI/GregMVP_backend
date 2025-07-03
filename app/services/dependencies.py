from fastapi import Depends, BackgroundTasks

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_subscription_repository import UserSubscriptionRepository
from app.repositories.wait_list_repository import WaitListRepository
from app.services import UserService, AuthService
from app.services.email_service import EmailService
from app.services.open_ai_service import OpenAIService
from app.services.s3_service import S3Service
from app.services.extractor import ExtractorService
from app.services.conversation_service import ConversationService
from app.services.wait_list_service import WaitListService


def get_user_service(
        user_repo: UserRepository = Depends(),
        subscription_repo: SubscriptionRepository = Depends(),
        role_repo: RoleRepository = Depends(),
        user_sub_repo: UserSubscriptionRepository = Depends(), email_service: EmailService = Depends()
) -> UserService:
    return UserService(user_repo, subscription_repo, role_repo, user_sub_repo, email_service)


def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service)

def get_s3_service() -> S3Service:
    return S3Service()

def get_email_service(background_tasks: BackgroundTasks = Depends()) -> EmailService:
    return EmailService(background_tasks)

def get_extractor_service() -> ExtractorService:
    return ExtractorService()

def get_open_ai_service() -> OpenAIService:
    return OpenAIService()

def get_conversation_service(conversation_repo: ConversationRepository = Depends(), open_ai: OpenAIService = Depends()) -> ConversationService:
    return ConversationService(conversation_repo, open_ai)

def get_wait_list_service(wait_list_repo: WaitListRepository = Depends(), email_service = Depends(EmailService)) -> WaitListService:
    from app.services.wait_list_service import WaitListService
    return WaitListService(wait_list_repo, email_service)