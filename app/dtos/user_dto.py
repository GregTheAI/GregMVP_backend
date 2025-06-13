from pydantic import Field

from app.entities import User


class UserResponseDto:
    def __init__(self, data: User):
        super().__init__(id=data.id, email=data.email)
    id: str
    email: str