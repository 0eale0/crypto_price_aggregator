from pydantic import BaseModel, EmailStr
from pydantic.fields import Field

"""
pydantic models for validation
"""


class UserSchemaRegistration(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class User(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        schema_extra = {"example": {"username": "string", "email": "your_email@gmail.com", "disabled": True}}


class UserInDB(User):
    hashed_password: str
