from sqlalchemy import (
    Column,
    Text,
    BIGINT,
    Boolean,
    String,
    ForeignKey,
    CheckConstraint,
    Float,
    BINARY,
    TIMESTAMP,
)
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import Configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()
engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)
session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(BIGINT, primary_key=True)
    email = Column(Text, unique=True)
    username = Column(Text, unique=True)
    hashed_password = Column(Text)
    is_google = Column(Boolean)
    favourites_crypto = relationship("UserFavouriteCrypto", lazy="select")
    posts = relationship("Post", lazy="select", backref=backref("posts", lazy="joined"))
    likes = relationship("Like", lazy="select", backref=backref("likes", lazy="joined"))
    is_admin = Column(Boolean, default=False)

    def dumps(self):
        result = {"username": self.username, "email": self.email}

        return result


class Exchange(Base):
    __tablename__ = "exchanges"
    id = Column(BIGINT, primary_key=True)
    name = Column(Text, unique=True)
    year_established = Column(Text)
    url = Column(Text)
    country = Column(Text)
    image_url = Column(Text)
    trust_score = Column(
        BIGINT, CheckConstraint("trust_score > 0", name="positive_trust_score")
    )
    coin_price = relationship(
        "CoinPrice",
        lazy="select",
        backref=backref("coin_price", lazy="joined"),
    )


class Cryptocurrency(Base):
    __tablename__ = "cryptocurrencies"
    id = Column(BIGINT, primary_key=True)
    name = Column(Text, unique=True)
    symbol = Column(Text, unique=True)
    image_url = Column(Text)
    crypto_info = Column(Text)

    def dumps(self):
        values_to_dump = ("name", "symbol", "image_url", "crypto_info")
        result = {key: getattr(self, key) for key in values_to_dump}

        return result


class CoinPrice(Base):
    __tablename__ = "coin_price"
    id = Column(BIGINT, primary_key=True)
    coin_id = Column(BIGINT, ForeignKey("cryptocurrencies.id"))
    exchange_id = Column(BIGINT, ForeignKey("exchanges.id"))
    price = Column(Float, CheckConstraint("price > 0", name="positive_price"))
    time = Column(TIMESTAMP)


class UserFavouriteCrypto(Base):
    __tablename__ = "users_favourite_cryptos"
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    coin_id = Column(BIGINT, ForeignKey("cryptocurrencies.id"))


class Post(Base):
    __tablename__ = "posts"
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    data = Column(Text)

    likes = relationship("Like", lazy="select", backref=backref("like", lazy="joined"))
    posts_comments = relationship(
        "PostsComment", lazy="select", backref=backref("posts_comments", lazy="joined")
    )


class PostPicture(Base):
    __tablename__ = "post_pictures"
    id = Column(BIGINT, primary_key=True)
    post_id = Column(BIGINT, ForeignKey("posts.id"), primary_key=True)
    picture_url = Column(Text)
    post = relationship("Post")


class Like(Base):
    __tablename__ = "likes"
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    post_id = Column(BIGINT, ForeignKey("posts.id"))


class PostsComment(Base):
    __tablename__ = "posts_comments"
    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    post_id = Column(BIGINT, ForeignKey("posts.id"))
    data = Column(String(100))


class PostTopics(Base):
    __tablename__ = "post_topics"
    id = Column(BIGINT, primary_key=True)
    post_id = Column(BIGINT, ForeignKey("posts.id"))
    coin_id = Column(BIGINT, ForeignKey("cryptocurrencies.id"))

# Base.metadata.create_all(engine)
