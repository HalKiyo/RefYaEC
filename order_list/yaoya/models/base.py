from __future__ import annotations

from typing import Protocol

class BaseDataModel(Protocol):
    def to_dict(self) -> dict[str, str]:
        pass

    @classmethod
    def from_dict(clas, data: dict[str, str]) -> BaseDataModel:
        pass

class NotFoundError(Exception):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        super().__init__(f"{user_id} not found")
