from app.entities import Subscription

from dataclasses import dataclass
from typing import Optional

@dataclass
class SubscriptionResponseDto:
    id: str
    plan_name: str
    plan_description: str
    price: float
    usage_limit: Optional[int]
    billing_cycle: Optional[str]
    is_active: bool

    @classmethod
    def from_entity(cls, data: Subscription) -> "SubscriptionResponseDto":
        return cls(
            id=str(data.id),
            plan_name=data.plan_name,
            plan_description=data.description,
            price=data.price,
            usage_limit=data.usage_limit,
            billing_cycle=data.billing_cycle,
            is_active=data.is_active
        )
