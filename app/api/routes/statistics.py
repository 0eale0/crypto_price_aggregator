from typing import List, Dict
from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.api.services.db_services import (
    get_session,
    get_current_active_user,
    user_favourite_cryptocurrency,
    get_cryptocurrency,
    delete_favourite_coin,
    update_favourites_coins,
)
from app.core.queries import min_max_average_price_by_exchange_for_each
from app.api.services.statistics_services import (
    get_aggregated_prices,
    get_symbol_avg_price_by_day,
)
from app.models.domain.users import CoinPrice, UserFavouriteCrypto, Cryptocurrency, User
from app.models.forms.users import NameCryptoForm

router = APIRouter()

# asc возрастающ


@router.get("/top_most_expensive_assets")
def top_10_most_expensive(db: Session = Depends(get_session)):
    coins = [
        c
        for c in db.query(CoinPrice)
        .order_by(desc(CoinPrice.time))
        .order_by(desc(CoinPrice.price))
        .limit(10)
        .all()
    ]
    return coins


@router.get("/top_cheapest_assets")
def top_10_cheapest(db: Session = Depends(get_session)):
    coins = [
        c
        for c in db.query(CoinPrice)
        .order_by(asc(CoinPrice.time))
        .order_by(desc(CoinPrice.price))
        .limit(10)
        .all()
    ]
    return coins


@router.get("/main_crypto")
def average_min_max_price_by_exchange():
    query = min_max_average_price_by_exchange_for_each
    try:
        prices = get_aggregated_prices(query)
        return prices
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Try again please"
        )


@router.post("/add_favourite_crypto")
def add_favourite_crypto_in_db(
    form: NameCryptoForm,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session),
):
    try:
        if current_user:
            if form.name_crypto:
                coin = get_cryptocurrency(db, form)
                return update_favourites_coins(current_user, coin, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return str(e)


@router.post("/delete_favourite_crypto")
def delete_favourite_crypto_in_db(
    form: NameCryptoForm,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        if current_user:
            if form.name_crypto:
                coin = get_cryptocurrency(db, form)
                user_with_fav_crypto = delete_favourite_coin(current_user, db, coin)
                return user_with_fav_crypto
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return str(e)


@router.get("/get_favourite_crypto")
def get_favourite_crypto_in_db(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        if current_user:
            user_with_fav_crypto = user_favourite_cryptocurrency(current_user, db)
            return user_with_fav_crypto
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return str(e)


@router.get("/charts/{symbol}")
def show_charts(symbol: str) -> List[Dict]:
    avg_prices = get_symbol_avg_price_by_day(symbol)
    return avg_prices
