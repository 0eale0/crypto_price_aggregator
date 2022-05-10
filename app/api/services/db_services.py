from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from models.forms.users import RegistrationForm, ChangeDataForm
from models.domain.users import User
from models.schemas.users import UserInDB
from api.services.auth_helpers import get_password_hash
from core.config import Configuration

engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def find_user_by_email(email: str, db: Session) -> bool:
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    return False


def find_user_by_username(username: str, db: Session) -> bool:
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    return None


def create_new_user(user: RegistrationForm, db: Session, is_google=False):
    user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password) if not is_google else None,
        is_google=is_google,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_user(current_user, new_user: ChangeDataForm, db: Session):
    user = db.query(User).filter(User.username == current_user["username"]).first()

    if new_user.username and not user.is_google:
        user.username = new_user.username
    if new_user.password and not user.is_google:
        user.hashed_password = get_password_hash(new_user.password)

    db.commit()
    db.refresh(user)
    return user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
