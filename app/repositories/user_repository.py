# app/db/repository/user.py
from fastapi import Depends

from app.core.storage.dependencies import get_pg_database
from app.entities.User import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db = Depends(get_pg_database)):
        super().__init__(User, db)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.get_by_field("email", email)
