import uuid

from sqlmodel import SQLModel, Field

from app.entities.audit_trail import AuditTrail


class UserRole(AuditTrail, SQLModel, table=True):
    __tablename__ = "user_roles"
    __table_args__ = {"extend_existing": True}

    name: str = Field(unique=True, index=True, max_length=50)
    description: str | None = Field(default=None, max_length=255)

    def __repr__(self) -> str:
        return f"<UserType(name={self.name}, description={self.description})>"
