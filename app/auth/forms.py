from fastapi import Request
from typing import List, Optional
from pydantic import EmailStr

class RegistrationForm:
    def __init__(self, request: Request):
        self.request = request
        self.username = None
        self.email = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.email = form.get('email')
        self.password = form.get('password')