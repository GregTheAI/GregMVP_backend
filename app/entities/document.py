import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel

from app.entities.audit_trail import AuditTrail


class Document(AuditTrail, SQLModel, table=True):
    __tablename__ = "documents"
    __table_args__ = {"extend_existing": True}

    user_id: uuid.UUID = Field(foreign_key="users.id")
    file_name: str = Field(max_length=255)
    file_type: str = Field(max_length=255)
    # activity_id: int | None = Field(default=None, foreign_key="activities.id")
    # document_type_id: int | None = Field(default=None, foreign_key="document_types.id")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    # source_id: int | None = Field(default=None, foreign_key="sources.id")
    file_path: str
    context: str | None = None
    summary: str | None = None
    processed: bool = False
    is_deleted: bool = False
    extracted_text: str | None = None
    processing_status: str | None = Field(default=None, max_length=255)
    processing_timestamp: datetime | None = None
    extraction_model: str | None = Field(default=None, max_length=255)