from pydantic import Field, BaseModel, EmailStr

from app.entities import User


class UserResponseDto:
    def __init__(self, data: User):
        super().__init__(id=data.id, email=data.email)
    id: str
    email: str

class RegisterUserDto(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)