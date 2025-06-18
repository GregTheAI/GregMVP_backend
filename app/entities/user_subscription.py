import uuid
from typing import ClassVar
from datetime import datetime

from sqlalchemy import ForeignKey, UUID, Column, DateTime
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field

from app.entities.audit_trail import AuditTrail


class UserSubscription(AuditTrail, SQLModel, table=True):
    __tablename__ = "user_subscriptions"
    __table_args__ = {"extend_existing": True}

    user_id: uuid.UUID = Field(foreign_key="users.id")
    subscription_id: uuid.UUID = Field(foreign_key="subscriptions.id")
    document_quota: int | None = Field(default=0, description="Number of documents processed or extracted")
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime
    is_active: bool = True

    subscription: ClassVar = relationship("Subscription", back_populates="user_subscriptions")
    user: ClassVar = relationship("User", back_populates="user_subscriptions")

