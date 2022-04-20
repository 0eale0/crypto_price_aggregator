from app.auth.schemas.user import User, UserInDB
from app.auth.db import SessionLocal

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def add_user(fake_db: dict, user: UserInDB):
    """
    DB call to add user
    """
    fake_db[user.username] = dict(user)


def is_exists(fake_db, username: str) -> bool:
    if username in fake_db:
        return True
    return False
