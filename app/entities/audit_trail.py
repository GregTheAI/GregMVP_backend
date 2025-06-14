from datetime import datetime, timezone
from sqlmodel import Field

class AuditTrail:
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)