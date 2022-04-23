from fastapi import Request
from typing import List, Optional
from pydantic import EmailStr, BaseModel


class RegistrationForm(BaseModel):
    username: str
    email: EmailStr
    password: str
    repeat_password: str

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.email = form.get('email')
        self.password = form.get('password')