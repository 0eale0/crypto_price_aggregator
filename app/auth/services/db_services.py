from app.auth.forms import RegistrationForm, ChangeDataForm, GoogleRegistrationForm
from app.auth.models import User

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.auth.local_configs import Configuration
from app.auth.schemas.user import UserInDB
from app.auth.services.auth_helpers import get_password_hash
import app.auth.models as models

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
    return None


def create_new_user(user: RegistrationForm, db: Session):
    user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password) if user.password else None
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_new_google_user(user: GoogleRegistrationForm, db: Session):
    email = user.email
    name = user.name

    user = models.GoogleUser(email=email, name=name)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_user(current_user, new_user: ChangeDataForm, db: Session):
    user = db.query(models.User).filter(User.username == current_user['username']).first()
    if new_user.username != "":
        user.username = new_user.new_username
        db.commit()
    if new_user.new_password != "":
        user.hashed_password = get_password_hash(new_user.new_password)
        db.commit()
    print(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
