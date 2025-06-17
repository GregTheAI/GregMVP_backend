from dataclasses import dataclass

from pydantic import EmailStr, BaseModel

from app.entities import User


class TokenData:
    email: str

    def __init__(self, email: str):
        self.email = email

class GoogleAuthUser:
    email: EmailStr
    name: str
    given_name: str
    family_name: str
    picture: str
    email_verified: bool
    locale: str

@dataclass
class OauthResponseDto:
    redirect_url: str

    @classmethod
    def from_entity(cls, data: str) -> "OauthResponseDto":
        return cls(redirect_url=data)



class LoginRequestDto(BaseModel):
    email : EmailStr
    password: str


@dataclass
class LoginResponseDto:
    id: str
    username: str
    token: str

    @classmethod
    def from_entity(cls, data: User, token: str) -> "LoginResponseDto":
        return cls(id=str(data.id),
                   username=data.username,
                   token=token)

