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
    first_name: str | None = Field(max_length=255, alias="firstName")
    last_name: str | None = Field(max_length=255, alias="lastName")
    password: str | None = None

class RegisterUser(RegisterUserDto):
    provider: str = "direct"
    profile_picture: str | None = None


class UpdateUserProfile(BaseModel):
    profile_picture: str | None = None
    first_name: str | None = Field(max_length=255)
    last_name: str | None = Field(max_length=255)