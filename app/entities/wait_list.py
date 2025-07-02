import uuid
from datetime import datetime
from typing import ClassVar

from pydantic import EmailStr
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

from app.entities.audit_trail import AuditTrail


class WaitList(AuditTrail, SQLModel, table=True):
    __tablename__ = "wait_list"
    __table_args__ = {"extend_existing": True}

    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_email_sent: bool = False