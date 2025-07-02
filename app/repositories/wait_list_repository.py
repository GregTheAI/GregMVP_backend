from fastapi import Depends

from app.core.storage.dependencies import get_pg_database
from app.entities.user import User
from app.entities.wait_list import WaitList
from app.repositories.base_repository import BaseRepository

class WaitListRepository(BaseRepository[User]):
    def __init__(self, db = Depends(get_pg_database)):
        super().__init__(WaitList, db)

    async def create_interest(self, interest: WaitList) -> User:
        return await self.create(interest.model_dump())

    async def user_has_already_registered(self, email: str) -> bool:
        return await self.exists_by_field("email", email)
