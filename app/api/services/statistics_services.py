from app.models.domain.users import engine
from typing import List, Dict


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
        return [{'error': str(e)}]


def get_aggregated_prices(query: str) -> List[Dict]:
    conn = engine.connect()
    try:
        aggregated_prices = conn.execute(query)
        return [r for r in aggregated_prices]
    except Exception as e:
        return [{'error': str(e)}]