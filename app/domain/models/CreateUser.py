from app.infrastructure.models.User import UserBase

from sqlmodel import Field

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)