from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.models.forms.users import NameCryptoForm
from app.models.domain.users import UserFavouriteCrypto, Cryptocurrency
from jose import jwt, JWTError
import os

from starlette import status

from app.models.forms.users import RegistrationForm, ChangeDataForm
from app.models.domain.users import User
from app.api.services.auth_helpers import (
    get_password_hash,
    oauth2_scheme,
    verify_password,
)
from app.core.config import Configuration
from app.models.schemas.tokens import TokenData

engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


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
    """
    Looks up a user in the database based on
    the username passed to the function.
    If a user with that username exists in the database,
    then returns an object of that user.
    If there is no such user in the database, then returns False.
    """
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    return False


def authenticate_user(username: str, password: str, db: Session):
    user = find_user_by_username(username, db)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_new_user(user: RegistrationForm, db: Session, is_google=False):
    """
    Creates a new user object based on
    the form data passed to the function,
    adds it to the database,
    and returns the created user object.
    """
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


def change_user(user: User, new_user: ChangeDataForm, db: Session):
    """
    Changes the username and password of the user.
    If the user is not a google account and has entered a new username,
    then the function changes the old username to the new one.
    If a new password is entered and the user is not a google account,
    then the function changes the old password to a new one.
    And the modified user object is returned.
    """
    if new_user.username and not user.is_google:
        user.username = new_user.username
    if new_user.password and not user.is_google:
        user.hashed_password = get_password_hash(new_user.password)

    db.commit()
    db.refresh(user)
    return user


async def get_current_user(
        token: str = Depends(oauth2_scheme), db=Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = find_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    return current_user


def user_favourite_cryptocurrency(current_user: User, db: Session):
    """
    Takes the current user object and returns
    that user's favorite cryptocurrencies
    from the database.
    """
    return (
        db.query(UserFavouriteCrypto)
            .filter(UserFavouriteCrypto.user_id == current_user.id)
            .all()
    )


def get_cryptocurrency(db: Session, form: NameCryptoForm):
    """
    Accepts a form with a cryptocurrency name field
    and returns an object of that cryptocurrency
    from the database.
    """
    return (
        db.query(Cryptocurrency)
            .filter(Cryptocurrency.symbol == form.name_crypto)
            .first()
    )


def delete_favourite_coin(current_user: User, db: Session, coin: Cryptocurrency):
    user_with_fav_crypto = (
        db.query(UserFavouriteCrypto)
            .filter(UserFavouriteCrypto.user_id == current_user.id)
            .filter(UserFavouriteCrypto.coin_id == coin.id)
            .first()
    )
    db.delete(user_with_fav_crypto)
    db.commit()
    current_favourite_cryptos = user_favourite_cryptocurrency(current_user, db)
    return current_favourite_cryptos


def update_favourites_coins(current_user: User, coin: Cryptocurrency, db: Session):
    user_with_fav_crypto = UserFavouriteCrypto(user_id=current_user.id, coin_id=coin.id)
    db.add(user_with_fav_crypto)
    db.commit()
    db.refresh(user_with_fav_crypto)
    favourites = user_favourite_cryptocurrency(current_user, db)
    return favourites
