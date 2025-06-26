import uuid
from typing import ClassVar

from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field

from app.entities import User
from app.entities.audit_trail import AuditTrail


class UserOnboarding(AuditTrail, SQLModel, table=True):
    __tablename__ = "user_onboarding"
    __table_args__ = {"extend_existing": True}

    user_id: uuid.UUID = Field(foreign_key="users.id")
    has_confirmed_profile: bool = Field(default=False)
    has_uploaded_customer_data: bool = Field(default=False)
    has_uploaded_customer_contacts: bool = Field(default=False)
    has_completed_intro: bool = Field(default=False)
    has_scheduled_meeting: bool = Field(default=False)

    user: ClassVar[User] = relationship("User", back_populates="onboarding")

