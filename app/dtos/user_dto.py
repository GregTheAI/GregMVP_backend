from dataclasses import dataclass

from pydantic import Field, BaseModel, EmailStr

from app.entities import User


# @dataclass
class UserResponseDto(BaseModel):
    id: str
    email: str
    first_name: str = Field(alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    username: str | None = Field(default=None)
    is_email_verified: bool = Field(default=False, alias="isEmailVerified")
    profile_picture: str | None = Field(default=None, alias="profilePicture")

    # @classmethod
    # def from_entity(cls, data: User) -> "UserResponseDto":
    #     return cls(id=str(data.id),
    #                email=str(data.email),
    #                first_name=data.first_name,
    #                last_name=data.last_name,
    #                is_email_verified=data.is_email_verified,
    #                profile_picture=data.profile_picture,
    #                  username=data.username)


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