from sqlalchemy import Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from .local_configs import Configuration
from sqlalchemy import create_engine


Base = declarative_base()
engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True)
    username = Column(Text, unique=True)
    hashed_password = Column(Text)

    def dumps(self):
        return {
            "email": self.email,
            "username": self.username
        }


Base.metadata.create_all(engine)
