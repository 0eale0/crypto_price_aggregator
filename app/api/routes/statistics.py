from typing import Dict, List
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
    get_recommendations,
)
from app.models.domain.users import CoinPrice, User
from app.models.forms.users import NameCryptoForm, DollarsMaxAmount
from app.api.services.statistics_services import get_standard_deviations


router = APIRouter()

UnauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authorized",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.get("/top_most_expensive_assets")
def top_10_most_expensive(db: Session = Depends(get_session)) -> list:
    """
    Refers to the CoinPrice table, sorts the coins in descending order of time,
    that is, the latest coins come first.\n
    Next, the coins are sorted in descending order of price,
    so that the coins with the highest prices will be at the beginning.\n
    Coins are limited to 10 pieces and are collected in a list.
    This list is then returned. It consists of the top 10 most expensive cryptocurrencies in recent times.
    """
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
def top_10_cheapest(db: Session = Depends(get_session)) -> list:
    """
    Refers to the CoinPrice table, sorts the coins in descending order of time,
    that is, the latest coins come first.\n
    The coins are then sorted in ascending order of price,
    so that the coins with the lowest prices will be at the beginning.\n
    Coins are limited to 10 pieces and are collected in a list.
    This list is then returned. It consists of the top 10 cheap cryptocurrencies in recent times.
    """
    coins = [
        c
        for c in db.query(CoinPrice)
        .order_by(desc(CoinPrice.time))
        .order_by(asc(CoinPrice.price))
        .limit(10)
        .all()
    ]
    return coins


@router.get("/main_crypto")
def average_min_max_price_by_exchange():
    """
      Returns average, min, max price of every asset in system by each exchange.\n
      Example Response:\n
          [
              {
              "coin_id": 1,
              "symbol": "BTC",
              "name": "binance",
              "max": 29322.18,
              "min": 29164.24,
              "avg": 29232.00090909091
              },\n
              {
              "coin_id": 1,
              "symbol": "BTC",
              "name": "ftx",
              "max": 29334,
              "min": 29167,
              "avg": 29226.125
              },\n
              {
              "coin_id": 1,
              "symbol": "BTC",
              "name": "kucoin",
              "max": 29342.3,
              "min": 29160.4,
              "avg": 29241.600000000002
    }
          ]
    """
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
    """
    This function adds new asset to the list of favourites.\n
    :param form: Request body (you need to pass just symbol, not full name(etc. "BTC", "ETH")\n
    :param current_user: authenticated with JWT token user\n
    :param db: connection with database\n
    :return: list of dicts with coin_id, user_id, or message that you already have
    """
    try:
        coin = get_cryptocurrency(db, form)
        return update_favourites_coins(current_user, coin, db)
    except Exception as e:
        return {"error": str(e)}


@router.post("/delete_favourite_crypto")
def delete_favourite_crypto_in_db(
    form: NameCryptoForm,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    This function deletes asset from the list of favourites assets.\n
    :param form: body of request\n
    :param current_user: authenticated with JWT token user\n
    :param db: connection with database\n
    :return: updated list of favourites(list of dicts with coin_id, user_id) if user is authenticated else 401 code
    """
    try:
        if form.name_crypto:
            coin = get_cryptocurrency(db, form)
            user_with_fav_crypto = delete_favourite_coin(current_user, db, coin)
            return user_with_fav_crypto
    except Exception:
        raise UnauthorizedException


@router.get("/get_favourite_crypto")
def get_favourite_crypto_in_db(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    This function returns list of favourites assets of user.\n
    :param current_user: authenticated with JWT token user\n
    :param db: connection with database\n
    :return: updated list of favourites(list of dicts with coin_id, user_id) if user is authenticated else 401 code\n
    """
    try:
        user_with_fav_crypto = user_favourite_cryptocurrency(current_user, db)
        return user_with_fav_crypto
    except Exception:
        raise UnauthorizedException


@router.get("/charts/{symbol}")
def show_charts(symbol: str) -> List[Dict]:
    """
    This function shows average prices of concrete asset.\n
    :param symbol:query parameter(etc. BTC)\n
    :return: updated list of favourites(list of dicts with coin_id, user_id) if user is authenticated else 401 code
    """
    avg_prices = get_symbol_avg_price_by_day(symbol)
    return avg_prices


@router.post("/recommendations")
def recommendations(
    form: DollarsMaxAmount, current_user: User = Depends(get_current_active_user)
):
    """
    This function shows the list of assets whose values are less than price in form.\n
    :param form: \n
    :param current_user: authenticated with JWT token user\n
    :return: updated list of favourites(list of dicts with coin_id, user_id) if user is authenticated else 401 code
    """
    try:
        return get_recommendations(form)
    except Exception:
        raise UnauthorizedException


@router.get("/standard_deviation/{symbol}")
def std_deviation(symbol: str):
    """
    Returns std_dev, average price of one asset by each day.\n
    Prices are aggregated only by date.\n
    :param: symbol: etc. "BTC", "ETC"(not bitcoin, ethereum)
    """
    std_devs = get_standard_deviations(symbol)
    return std_devs
