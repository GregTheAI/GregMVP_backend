from fastapi import Depends

from app.core.storage.dependencies import get_pg_database
from app.dtos.subscription_dto import SubscriptionResponseDto
from app.entities import Subscription
from app.repositories.base_repository import BaseRepository
from app.repositories.user_repository import UserRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    """Repository for subscription-related operations."""

    def __init__(self, db = Depends(get_pg_database)):
        super().__init__(Subscription, db)

    async def get_subscription_by_name(self, plan_name: str) -> SubscriptionResponseDto | None:
        subscription = await self.get_by_field("plan_name", plan_name)
        if subscription is None:
            return None
        return SubscriptionResponseDto.from_entity(subscription)
