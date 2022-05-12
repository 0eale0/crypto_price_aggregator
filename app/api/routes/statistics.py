from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from sqlalchemy.sql.functions import func
from app.api.services.db_services import get_session, engine
from app.core.queries import min_max_average_price_by_exchange_for_each, recommendations
from app.api.services.statistics_services import get_aggregated_prices, get_standard_deviations
from app.models.domain.users import CoinPrice, UserFavouriteCrypto, Cryptocurrency, User
from app.models.forms.users import NameFavouriteCryptoForm, MaxPriceCryptoForm

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
        .order_by(desc(CoinPrice.time))
        .order_by(asc(CoinPrice.price))
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
    request: Request, form: NameFavouriteCryptoForm, db: Session = Depends(get_session)
):
    try:
        current_user = request.session.get("user")
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if user:
            if form.name_crypto:
                coin = (
                    db.query(Cryptocurrency)
                    .filter(Cryptocurrency.symbol == form.name_crypto)
                    .first()
                )
                user_with_fav_crypto = UserFavouriteCrypto(
                    user_id=user.id, coin_id=coin.id
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


@router.post("/delete_favourite_crypto")
def delete_favourite_crypto_in_db(
    request: Request, form: NameFavouriteCryptoForm, db: Session = Depends(get_session)
):
    try:
        current_user = request.session.get("user")
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if user:
            if form.name_crypto:
                coin = (
                    db.query(Cryptocurrency)
                    .filter(Cryptocurrency.symbol == form.name_crypto)
                    .first()
                )
                user_with_fav_crypto = (
                    db.query(UserFavouriteCrypto)
                    .filter(UserFavouriteCrypto.user_id == user.id)
                    .filter(UserFavouriteCrypto.coin_id == coin.id)
                    .first()
                )
                db.delete(user_with_fav_crypto)
                db.commit()
                return user_with_fav_crypto
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return str(e)


@router.get("/get_favourite_crypto")
def get_favourite_crypto_in_db(request: Request, db: Session = Depends(get_session)):
    try:
        current_user = request.session.get("user")
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if user:
            user_with_fav_crypto = (
                db.query(UserFavouriteCrypto)
                .filter(user.id == UserFavouriteCrypto.user_id)
                .all()
            )
            return user_with_fav_crypto
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return str(e)


@router.post("/add_price_for_recommendations")
def add_price_for_recommendations(request: Request, form: MaxPriceCryptoForm):
    """
    🤢🤢🤢🤢🤢🤢🤢🤢🤢
    """
    # TODO переписать в ORM, сделать проверку текущего юзера через токен
    try:
        current_user = request.session.get("user")
        if current_user:
            conn = engine.connect()
            q = ("select"
                 " c.symbol, avg(cp.price) as price"
                 " from coin_price cp"
                   " join cryptocurrencies c on c.id = cp.coin_id"
                   f" where current_date - cp.time <= interval '5 minutes' and cp.price<={form.price}"
                   " group by c.symbol"
                   " order by price desc"
)
            # today = datetime.date.today()
            # res = db.query(CoinPrice)\
            #     .join(Cryptocurrency)\
            #     .filter(today - datetime.date(CoinPrice.time), CoinPrice.price <= int(form.price))\
            #     .values(Cryptocurrency.symbol,
            #             )\
            #     .group_by(Cryptocurrency.symbol).order_by(desc(CoinPrice.price))
            get_recommendations = conn.execute(q)
            return [r for r in get_recommendations]

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return str(e)


@router.get("/standard_deviation")
def std_deviation():
    std_devs = get_standard_deviations()
    return std_devs