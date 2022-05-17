from app.models.domain.users import engine
from typing import List, Dict


def get_aggregated_prices(query: str) -> List[Dict]:
    conn = engine.connect()
    try:
        aggregated_prices = conn.execute(query)
        return [r for r in aggregated_prices]
    except Exception as e:
        return e


def get_symbol_avg_price_by_day(symbol: str):
    conn = engine.connect()
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
