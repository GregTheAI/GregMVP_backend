from fastapi import Depends

from app.core.storage.dependencies import get_pg_database
from app.entities import UserSubscription
from app.repositories.base_repository import BaseRepository


class UserSubscriptionRepository(BaseRepository[UserSubscription]):
    """Repository for subscription-related operations."""

    def __init__(self, db = Depends(get_pg_database)):
        super().__init__(UserSubscription, db)

    async def create_user_subscription(self, user_subscription: UserSubscription) -> UserSubscription:
        return await self.create(user_subscription.model_dump())
