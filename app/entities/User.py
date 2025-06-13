import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)
    username: str = Field(unique=True, index=True, max_length=50)
    password: str
    is_active: bool = True
    is_superuser: bool = False
