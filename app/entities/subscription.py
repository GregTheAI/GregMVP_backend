import uuid

from sqlmodel import SQLModel, Field

from app.entities.audit_trail import AuditTrail


class Subscription(AuditTrail, SQLModel, table=True):
    __tablename__ = "subscriptions"
    __table_args__ = {"extend_existing": True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    plan_name: str = Field(index=True, max_length=100)
    description: str | None = Field(default=None, index=True, max_length=255)
    price: float = Field(default=0, description="Price in the smallest currency unit (e.g., cents for USD)")
    usage_limit: int | None = Field(default=100, description="Maximum number of API calls or other usage limits")
    billing_cycle: str | None = Field(default="monthly", index=True)  # e.g., "monthly", "yearly"
    is_active: bool = True

    def __repr__(self) -> str:
        return f"<Subscription(name={self.plan_name}, price={self.price}, is_active={self.is_active}, usage_limit={self.usage_limit}, billing_cycle={self.billing_cycle}, description={self.description})>"
