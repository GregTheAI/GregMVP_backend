from fastapi import Depends, BackgroundTasks

from app.core.log_config import configure_logger
from app.core.storage.dependencies import get_pg_database
from app.dtos.activity_status import ActivityStatus
from app.dtos.register_interest_dto import RegisterInterestDto, RegisterInterestResponse
from app.entities.wait_list import WaitList
from app.repositories.wait_list_repository import WaitListRepository
from app.services.email_service import EmailService
from app.utils.helpers.email.wait_list import send_wait_list_html_email


class WaitListService:

    def __init__(self, wait_list_repo=Depends(WaitListRepository), email_service=Depends(EmailService)):
        self.logger = configure_logger(__name__)
        self.wait_list_repo: WaitListRepository = wait_list_repo
        self.email_service: EmailService = email_service
        self.db = get_pg_database()

    async def send_wait_list_confirmation_email(self, email: str) -> None:
        """Send a confirmation email to the user."""
        try:
            self.logger.info(f"Sending email to {email}")

            email = email.strip()
            name = email.split('@')[0].capitalize()
            html_content = send_wait_list_html_email(name)
            self.email_service.send_email_background(to_email=email,
                                                           subject="Registration Confirmation",
                                                           html_content=html_content)
        except Exception as e:
            self.logger.error(f"Failed to send confirmation email to {email}: {e}")

    async def create_interest(self, request: RegisterInterestDto) -> ActivityStatus:
        try:
            email_str = str(request.email)
            existing_interest = await self.wait_list_repo.user_has_already_registered(email=email_str)
            if existing_interest:
                return ActivityStatus(code=409, message="Interest already registered")

            request = WaitList(email=email_str)
            created_interest = await self.wait_list_repo.create_interest(request)
            if created_interest is None:
                return ActivityStatus(code=424, message="Failed to register interest")

            # Send confirmation email
            await self.send_wait_list_confirmation_email(email_str)

            return ActivityStatus(code=201, message="Interest registered successfully",
                                  data=RegisterInterestResponse(email=email_str))
        except Exception as e:
            return ActivityStatus(code=500, message="Failed to register interest")
