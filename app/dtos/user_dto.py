from dataclasses import dataclass

from pydantic import Field, BaseModel, EmailStr

from app.entities import User


@dataclass
class UserResponseDto:
    id: str
    email: str

    @classmethod
    def from_entity(cls, data: User) -> "UserResponseDto":
        return cls(id=str(data.id),
                   email=str(data.email))


class RegisterUserDto(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
