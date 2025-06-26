import uuid
from datetime import datetime
from typing import ClassVar

from pydantic import EmailStr
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

from app.entities import UserSubscription
from app.entities.audit_trail import AuditTrail
from app.entities.user_onboarding import UserOnboarding


class User(AuditTrail, SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    email: EmailStr = Field(unique=True, index=True, max_length=255)
    first_name: str | None = Field(default=None, index=True, max_length=255)
    last_name: str | None = Field(default=None, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=50)
    password: str | None = Field(default=None, index=True)
    profile_picture: str | None = Field(default=None, index=True)
    provider: str = Field(default="direct", index=True, max_length=50)
    role_id: uuid.UUID | None = Field(foreign_key="user_roles.id")
    is_active: bool = True
    is_superuser: bool = False
    is_email_verified: bool = False
    last_login: datetime = Field(default_factory=datetime.utcnow)

    user_subscriptions: ClassVar[UserSubscription] = relationship("UserSubscription", back_populates="user")
    onboarding: ClassVar[UserOnboarding] = relationship("UserOnboarding", back_populates="user")

