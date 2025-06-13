from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    def __init__(self, message: str, code: int, data: Optional[T] = None, errors: Optional[dict] = None):
        super().__init__(message=message, code=code, data=data, errors=errors)
    message: str
    code: int
    data: Optional[T] = None
    errors: Optional[dict] = None
