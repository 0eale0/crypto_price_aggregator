import aiohttp
from fastapi import Depends, HTTPException, status, APIRouter

from starlette.requests import Request

from app.models.domain.users import Cryptocurrency
from app.models.forms.users import NameCryptoForm
from app.api.services.db_services import get_session, get_current_active_user
from sqlalchemy.orm import Session
from app.models.domain.users import User

router = APIRouter()


@router.post("/get_crypto_info")
def get_crypto_info(
    form: NameCryptoForm, db: Session = Depends(get_session)
) -> dict[str, str] | None:
    try:
        description = (
            db.query(Cryptocurrency)
            .filter(Cryptocurrency.name == form.name_crypto)
            .first()
        )
        return {"symbol": form.name_crypto, "description": str(description.crypto_info)}
    except Exception as e:
        return
