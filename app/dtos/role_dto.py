from dataclasses import dataclass

from app.entities import UserRole


@dataclass
class UserRoleResponseDto:
    """Data Transfer Object for User Role."""
    id: str
    role_name: str

    @classmethod
    def from_entity(cls, data: UserRole) -> "UserRoleResponseDto":
        return cls(
            id=str(data.id),
            role_name=data.name
        )