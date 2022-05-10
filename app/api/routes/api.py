from fastapi import APIRouter

from app.api.routes import coin
from app.api.routes import authentication
from app.api.routes import crypto_websockets
from app.api.routes import top_10
from app.api.routes import crud

router = APIRouter()

router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(crypto_websockets.router, tags=["api"], prefix="")
router.include_router(top_10.router, tags=["top10"], prefix="")
router.include_router(coin.router, tags=["coin"], prefix="")

#  Crud routers
router.include_router(crud.router_cryptocurrency)
router.include_router(crud.router_user)
router.include_router(crud.router_exchange)
router.include_router(crud.router_coin_price)
router.include_router(crud.router_user_favourite_crypto)
router.include_router(crud.router_post)
router.include_router(crud.router_post_picture)
router.include_router(crud.router_like)
router.include_router(crud.router_posts_comment)
