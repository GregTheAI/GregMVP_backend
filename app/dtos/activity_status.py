from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")

class ActivityStatus(BaseModel, Generic[T]):
    def __init__(self, message: str, code: int, data: Optional[T] = None):
        super().__init__(message=message, code=code, data=data)

    @property
    def is_success(self) -> bool:
        return str(self.code).startswith("2")

    isSuccess = is_success
    message: str
    code: int
    data: Optional[T] | None = None