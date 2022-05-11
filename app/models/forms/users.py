from pydantic import EmailStr, BaseModel, validator


class UserValidation:
    @validator("username")
    def check_username(cls, v):
        if not len(v) >= 3:
            raise ValueError("Username should be at least 3 symbols")

        return v.title()

    @validator("password")
    def password_len(cls, v, values, **kwargs):
        if not len(v) >= 4:
            raise ValueError("Password length should be at least 4 symbols")
        return v


class RegistrationForm(BaseModel):
    username: str
    email: EmailStr
    password: str
    repeat_password: str

    async def load_data(self):
        form = await self.request.form()
        print(form)
        self.username = form.get("username")
        self.email = form.get("email")
        self.password = form.get("password")

    @validator("username")
    def check_username(cls, v):
        if not len(v) >= 3:
            raise ValueError("Username should be at least 3 symbols")

        return v.title()

    @validator("password")
    def password_len(cls, v, values, **kwargs):
        if not len(v) >= 4:
            raise ValueError("Password length should be at least 4 symbols")
        return v

    @validator("repeat_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class ChangeDataForm(BaseModel):
    username: str
    password: str

    async def load_data(self):
        form = await self.request.form()

    @validator("username")
    def check_username(cls, v):
        if not len(v) >= 3:
            raise ValueError("Username should be at least 3 symbols")

        return v.title()

    @validator("password")
    def password_len(cls, v, values, **kwargs):
        if not len(v) >= 4:
            raise ValueError("Password length should be at least 4 symbols")
        return v


class NameCryptoForm(BaseModel):
    name_crypto: str


class NameFavouriteCryptoForm(BaseModel):
    name_crypto: str


class MaxPriceCryptoForm(BaseModel):
    price: str
