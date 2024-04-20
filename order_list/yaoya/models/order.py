from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime

from yaoya.models.base import BaseDataModel
from yaoya.models.item import Item


@dataclass(frozen=True)
class Order(BaseDataModel):
    order_id: str
    user_id: str
    total_price: int
    ordered_at: datetime

    def to_dict(self) -> dict[str, str]:
        return dict(
            order_id=self.order_id,
            user_id=self.user_id,
            total_price=str(self.total_price),
            ordered_at=self.ordered_at.isoformat()
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Order:
        return Order(
            order_id=data["order_id"],
            user_id=data["user_id"],
            total_price=int(data["total_price"]),
            ordered_at=datetime.fromisoformat(data["ordered_at"])
        )
