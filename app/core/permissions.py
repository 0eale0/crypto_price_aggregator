from fastapi import Depends, HTTPException

from app.api.services.db_services import get_current_active_user
from app.models.domain.users import User


def is_admin(current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:  # pragma: no cover
        raise HTTPException(403, "You don't have access for this method")


def is_user(current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(403, "You don't have access for this method")
