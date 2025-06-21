import uuid

from sqlmodel import SQLModel, Field

from app.entities.audit_trail import AuditTrail


class Conversation(AuditTrail, SQLModel, table=True):
    __tablename__ = "conversations"
    __table_args__ = {"extend_existing": True}

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    role: str = Field(nullable=False)
    session_id: str = Field(nullable=False, index=True)
    content: str = Field(nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)
    # file_refs: dict | None = Field(default=None)