from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.api.services.db_services import get_session
from app.models.domain.users import CoinPrice
from app.core.queries import min_max_average_price_by_exchange_for_each
from app.api.services.statistics_services import get_aggregated_prices
router = APIRouter()


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
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Try again please"
        )