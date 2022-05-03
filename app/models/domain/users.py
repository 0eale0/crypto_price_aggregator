from sqlalchemy import (
    Column,
    Text,
    Integer,
    Boolean,
    String,
    ForeignKey,
    CheckConstraint, Float,
)
from sqlalchemy.ext.declarative import declarative_base
from core.config import Configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()
engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)
session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True)
    username = Column(Text, unique=True)
    hashed_password = Column(Text)
    is_google = Column(Boolean)
    favourites_crypto = relationship(
        "UserFavouriteCrypto",
        lazy="select",
        backref=backref("users_fav_crypto", lazy="joined"),
    )
    posts = relationship(
        "Post", lazy="select", backref=backref("posts", lazy="joined")
    )
    likes = relationship(
        "Like", lazy="select", backref=backref("likes", lazy="joined")
    )

    def dumps(self):
        result = {"username": self.username, "email": self.email}

        return result


class Exchange(Base):
    __tablename__ = "exchanges"
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    year_established = Column(Text)
    url = Column(Text)
    country = Column(Text)
    image_url = Column(Text)
    trust_score = Column(
        Integer, CheckConstraint("trust_score > 0", name="positive_trust_score")
    )

    cryptos = relationship(
        "Cryptocurrency",
        lazy="select",
        backref=backref("cryptocurrency", lazy="joined"),
    )


class Cryptocurrency(Base):
    __tablename__ = "cryptocurrencies"
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    symbol = Column(Text, unique=True)
    image_url = Column(Text)
    exchange_id = Column(Integer, ForeignKey("exchanges.id"))
    price = Column(Float, CheckConstraint("price > 0", name="positive_price"))


class UserFavouriteCrypto(Base):
    __tablename__ = "users_favourite_cryptos"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    coin_id = Column(Integer, ForeignKey("cryptocurrencies.id"))


class Post(Base):
    """
    #TO DO: image должен принимать другой тип
    """
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    data = Column(Text)
    image = Column(Text)

    likes = relationship("Like", lazy="select", backref=backref("like", lazy="joined"))
    posts_comments = relationship("PostsComment", lazy="select", backref=backref("posts_comments", lazy="joined"))


class PostPicture(Base):
    __tablename__ = "post_pictures"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    post = relationship("Post")


class Like(Base):
    __tablename__ = "likes"
    like_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))


class PostsComment(Base):
    __tablename__ = "posts_comments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    data = Column(String(100))


Base.metadata.create_all(engine)
