from models.domain.users import engine
from typing import List, Dict
from app.models.forms.users import DollarsMaxAmount


def get_connection():
    conn = engine.connect()
    return conn


def get_recommendations(form: DollarsMaxAmount):
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


def get_aggregated_prices(query: str) -> List[Dict]:
    conn = get_connection()
    try:
        aggregated_prices = conn.execute(query)
        return [r for r in aggregated_prices]
    except Exception as e:
        return e


def get_standard_deviations(symbol: str) -> List[Dict]:
    # отклонение цены от среднего значения(средняя по всем биржами)
    std_deviation = (
        "select"
        " c.id, c.symbol, date(cp.time) date, avg(cp.price) avg_price, stddev(cp.price) std_dev"
        " from coin_price cp"
        " left join cryptocurrencies c on c.id = cp.coin_id"
        f" where c.symbol='{symbol}'"
        " group by cp.coin_id, c.symbol, c.id, date"
        " order by cp.coin_id"
    )
    conn = engine.connect()
    try:
        std_devs = conn.execute(std_deviation)
        return [r for r in std_devs]
    except Exception as e:
        return [{"error": str(e)}]


def get_symbol_avg_price_by_day(symbol: str):
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
