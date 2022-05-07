import datetime
from starlette.requests import Request

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.api.services.db_services import get_session
from app.models.domain.users import CoinPrice, UserFavouriteCrypto, Cryptocurrency, User
from app.models.forms.users import NameFavouriteCryptoForm

router = APIRouter()
# asc возрастающ


@router.get("/top_most_expensive_assets")
def top_10_most_expensive(db: Session = Depends(get_session)):
    coins = [
        c.dumps()
        for c in db.query(Cryptocurrency)
        .order_by(desc(Cryptocurrency.price))
        .order_by(desc(Cryptocurrency.time))
        .limit(10)
        .all()
    ]
    return coins


@router.get("/top_cheapest_assets")
def top_10_cheapest(db: Session = Depends(get_session)):
    coins = [
        c.dumps()
        for c in db.query(Cryptocurrency)
        .order_by(asc(Cryptocurrency.price))
        .order_by(desc(Cryptocurrency.time))
        .limit(10)
        .all()
    ]
    return coins


@router.post("/favourite_crypto")
def add_favourite_crypto_in_db(request: Request, form: NameFavouriteCryptoForm, db: Session = Depends(get_session)):
    try:
        current_user = request.session.get("user")
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if user:
            if form.name_crypto:
                coin = db.query(Cryptocurrency).filter(Cryptocurrency.symbol == form.name_crypto).first()
                user_with_fav_crypto = UserFavouriteCrypto(
                    user_id=user.id,
                    coin_id=coin.id
                )
                db.add(user_with_fav_crypto)
                db.commit()
                db.refresh(user_with_fav_crypto)
                return user_with_fav_crypto
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return str(e)
