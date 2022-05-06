import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.api.services.db_services import get_session
from app.models.domain.users import Cryptocurrency

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
