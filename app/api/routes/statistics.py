from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.api.services.db_services import get_session
from app.models.domain.users import CoinPrice, engine

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
def average_min_max_price_by_exchange(db: Session = Depends(get_session)):
    raw = ("select coin_id, max(price), min(price)"
           "from coin_price"
           " where current_date - coin_price.time <= interval '5 minutes'"
           "group by coin_id order by coin_id")

    conn = engine.connect()
    try:
        res = conn.execute(raw)
        return [r for r in res]
    except Exception as e:
        print(e)