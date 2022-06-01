from app.models.domain.users import engine
from fastapi import Depends
from sqlalchemy.engine.base import Connection
from app.models.forms.users import DollarsMaxAmount
from typing import Union, List, Dict


def get_connection() -> Connection:
    conn = engine.connect()
    return conn


def get_recommendations(form: DollarsMaxAmount) -> Union[List[Dict], str]:
    conn = get_connection()
    q = (
        "select"
        " c.symbol, avg(cp.price) as price"
        " from coin_price cp"
        " join cryptocurrencies c on c.id = cp.coin_id"
        f" where current_date - cp.time <= interval '5 minutes' and cp.price<={form.amount_of_money}"
        " group by c.symbol"
        " order by price desc"
    )
    try:
        recs = conn.execute(q)
        return [r for r in recs]
    except Exception as e:
        return str(e)


def get_aggregated_prices(query: str) -> Union[List[Dict], Exception]:
    conn = get_connection()
    try:
        aggregated_prices = conn.execute(query)
        return [r for r in aggregated_prices]
    except Exception as e:
        return e


def get_symbol_avg_price_by_day(symbol: str) -> Union[List[Dict], Exception]:
    conn = get_connection()
    avg_prices_by_day = (
        "select"
        " c.symbol, avg(price) avg_price, date(time) as day"
        " from coin_price cp"
        " join cryptocurrencies c on c.id = cp.coin_id"
        f" where symbol='{symbol.upper()}'"
        " group by c.symbol, date(time)"
        " order by day"
    )
    try:
        avg_prices = conn.execute(avg_prices_by_day)
        return [r for r in avg_prices]
    except Exception as e:
        return e


def get_standard_deviations(symbol: str) -> Union[List[Dict], str]:
    conn = get_connection()
    std_devs = (
        "select "
        "c.id, c.symbol, date(cp.time) as date, avg(cp.price), stddev(cp.price) std_dev "
        "from coin_price cp "
        "left join cryptocurrencies c on c.id = cp.coin_id "
        f"where c.symbol='{symbol.upper()}' "
        "group by cp.coin_id, c.symbol, c.id, date "
        "order by cp.coin_id"
    )
    try:
        res = conn.execute(std_devs)
        return [r for r in res]
    except Exception as e:
        return str(e)
