from pydantic import BaseModel, EmailStr
from typing import Optional

"""
Pydantic models for validation
"""


class User(BaseModel):
    username: str
    email: EmailStr
    disabled: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "string",
                "email": "your_email@gmail.com",
                'disabled': True
            }
        }


class UserInDB(User):
    hashed_password: str
