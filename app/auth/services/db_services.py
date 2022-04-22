from auth.forms import RegistrationForm
from auth.models import User

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth.local_configs import Configuration
from auth.services.auth_helpers import get_password_hash

engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



def is_exists(fake_db, username: str) -> bool:
    if username in fake_db:
        return True
    return False


def create_new_user(user: RegistrationForm, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
