import uuid
from typing import ClassVar

from sqlalchemy.orm import relationship
from sqlmodel import Field, SQLModel

from app.entities.audit_trail import AuditTrail


class Customer(AuditTrail, SQLModel, table=True):
    __tablename__ = "customers"
    __table_args__ = {"extend_existing": True}

    name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, unique=True, index=True)
    phone: str | None = Field(default=None, index=True)
    address: str | None = Field(default=None)
    is_active: bool = Field(default=True, nullable=False)

    user_id: uuid.UUID | None = Field(foreign_key="users.id", index=True)
    user: ClassVar = relationship("User", back_populates="customers")
    contacts: ClassVar = relationship("Contact", back_populates="customer")


