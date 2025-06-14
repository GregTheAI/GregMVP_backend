from fastapi import Depends

from app.core.storage.dependencies import get_pg_database
from app.dtos.role_dto import UserRoleResponseDto
from app.entities import UserRole
from app.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[UserRole]):
    """Repository for role-related operations."""

    def __init__(self, db = Depends(get_pg_database)):
        super().__init__(UserRole, db)

    async def get_role_by_name(self, name: str) -> UserRoleResponseDto | None:
        """Get a role by its name."""
        role = await self.get_by_field("name", name)
        if role is None:
            return None

        return UserRoleResponseDto.from_entity(role)