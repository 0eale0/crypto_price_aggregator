from auth.forms import RegistrationForm
from auth.models import User

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth.local_configs import Configuration
from auth.schemas.user import UserInDB
from auth.services.auth_helpers import get_password_hash
import auth.models as models

engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def find_user_by_email(email: str, db: Session) -> bool:
    user = db.query(models.User).filter(User.email == email).first()
    if user:
        return user
    return False


def find_user_by_username(username: str, db: Session) -> bool:
    user = db.query(models.User).filter(User.username == username).first()
    if user:
        return user
    return False


def create_new_user(user: RegistrationForm, db: Session):
    user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
