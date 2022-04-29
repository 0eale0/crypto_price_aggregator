from sqlalchemy import Column, Text, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from core.config import Configuration
from sqlalchemy import create_engine


Base = declarative_base()
engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True)
    username = Column(Text, unique=True)
    hashed_password = Column(Text)
    is_google = Column(Boolean)

    def dumps(self):
        result = {"username": self.username,
                  "email": self.email}

        return result


# Base.metadata.create_all(engine)
