from fastapi import APIRouter

from app.api.routes import authentication
from app.api.routes import crypto_websockets

router = APIRouter()

router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(crypto_websockets.router, tags=["api"], prefix="")
