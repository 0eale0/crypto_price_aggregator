from fastapi import APIRouter

from app.api.routes import coin
from app.api.routes import authentication
from app.api.routes import crypto_websockets
from app.api.routes import top_10

router = APIRouter()

router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(crypto_websockets.router, tags=["api"], prefix="")
router.include_router(top_10.router, tags=["top10"], prefix="")
router.include_router(coin.router, tags=["coin"], prefix="")
