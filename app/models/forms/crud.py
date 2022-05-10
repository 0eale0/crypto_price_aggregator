from pydantic import BaseModel, EmailStr, validator
from pydantic.schema import Optional, Dict
import datetime

class FormForCrud(BaseModel):
    class Config:
        orm_mode = True


class Cryptocurrency(FormForCrud):
    id: int
    name: str
    symbol: str
    image_url: str
    crypto_info: str


class User(FormForCrud):
    id: int
    email: EmailStr
    username: str
    is_google: bool


class UserCreate(FormForCrud):
    username: str
    email: EmailStr
    password: str


class CoinPrice(FormForCrud):
    id: int
    coin_id: int
    exchange_id: int
    price: float
    time: datetime.datetime


class Exchange(FormForCrud):
    id: int
    name: str
    year_established: str
    url: str
    country: str
    image_url: str
    trust_score: int

    @validator('trust_score')
    def trust_score_not_negative(cls, v):
        if v > 0:
            return v.title

        raise ValueError("trust_score should be > 0")


class UserFavouriteCrypto(FormForCrud):
    id: int
    user_id: int
    coin_id: int


class Post(FormForCrud):
    id: int
    user_id: int
    data: str


class PostPicture(FormForCrud):
    id: int
    post_id: int
    picture_url: str
