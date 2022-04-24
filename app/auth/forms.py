from pydantic import EmailStr, BaseModel, ValidationError, validator


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

    @validator('username')
    def check_username(cls, v):
        if not len(v) >= 3:
            raise ValueError('Username should be at least 3 symbols')

        return v.title()

    @validator('password')
    def password_len(cls, v, values, **kwargs):
        if not len(v) >= 4:
            raise ValueError('Password length should be at least 4 symbols')
        return v

    @validator('repeat_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class GoogleRegistrationForm(BaseModel):
    name: str
    email: EmailStr

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get('name')
        self.email = form.get('email')


class ChangeDataForm(BaseModel):
    username: str
    new_username: str
    email: EmailStr
    password: str
    new_password: str

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.email = form.get('email')
        self.password = form.get('password')

    def username_length_is_valid(self) -> bool or dict:
        return (len(self.username) >= 3) and (len(self.new_username) >= 3 or len(self.new_username) >= 0)

    def password_length_is_valid(self):
        return (len(self.password) >= 4) and (len(self.new_password) >= 4 or len(self.new_password) == 0)
