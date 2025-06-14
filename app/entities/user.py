import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.entities.audit_trail import AuditTrail


class User(AuditTrail, SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    full_name: str | None = Field(default=None, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=50)
    password: str = Field(index=True)
    subscription_id: uuid.UUID = Field(foreign_key="subscriptions.id")
    role_id: uuid.UUID | None = Field(foreign_key="user_roles.id")
    is_active: bool = True
    is_superuser: bool = False
    last_login: datetime = Field(default_factory=datetime.utcnow)
