import aiohttp
from fastapi import Depends, HTTPException, status, APIRouter

from starlette.requests import Request

from models.forms.users import NameCryptoForm
from api.crypto_sites.coingecko_api import get_coin_description


router = APIRouter()


@router.post("/get_crypto_info")
async def get_crypto_info(request: Request, form: NameCryptoForm):
    try:
        user = request.session.get("user")
        if user:
            description = await get_coin_description(form.name_crypto)
            return description
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as error:
        return
