import uuid
from typing import ClassVar

from sqlalchemy.orm import relationship
from sqlmodel import Field, SQLModel

from app.entities.audit_trail import AuditTrail


class Contact(AuditTrail, SQLModel, table=True):
    __tablename__ = "contacts"
    __table_args__ = {"extend_existing": True}

    first_name: str = Field(nullable=False, index=True)
    last_name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, unique=True, index=True)
    phone: str | None = Field(default=None, index=True)
    address: str | None = Field(default=None)
    is_active: bool = Field(default=True, nullable=False)
    customer_id: uuid.UUID | None = Field(foreign_key="customers.id", index=True)

    customer: ClassVar = relationship("Customer", back_populates="contacts")
