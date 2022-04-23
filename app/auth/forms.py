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

    def username_length_is_valid(self) -> bool or dict:
        return len(self.username) >= 3

    def password_length_is_valid(self):
        return len(self.password) >= 4

    def passwords_equal_is_valid(self):
        return self.password == self.repeat_password
