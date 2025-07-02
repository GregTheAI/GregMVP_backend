from pydantic import Field, BaseModel, EmailStr


class RegisterInterestDto(BaseModel):
    email: EmailStr = Field(max_length=255)

class RegisterInterestResponse(BaseModel):
    email: str | None