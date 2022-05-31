from pydantic import BaseModel, EmailStr, validator, NonNegativeInt
from pydantic.schema import Optional, Dict
import datetime


class FormForCrud(BaseModel):
    class Config:
        orm_mode = True


class Cryptocurrency(FormForCrud):
    id: int
    name: str
    symbol: str
    image_url: Optional[str]
    crypto_info: Optional[str]


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
    year_established: Optional[str]
    url: Optional[str]
    country: Optional[str]
    image_url: Optional[str]
    trust_score: Optional[NonNegativeInt]


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


class Like(FormForCrud):
    id: int
    user_id: int
    post_id: int


class PostsComment(FormForCrud):
    id: int
    user_id: int
    post_id: int
    data: str


class PostTopics(FormForCrud):
    id: int
    post_id: int
    coin_id: int
