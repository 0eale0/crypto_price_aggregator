from app.models.domain.users import engine
from app.core.queries import(min_max_average_price_by_exchange_for_each,
                             recommendations,
                             std_deviation)
from typing import List, Dict


def get_standard_deviations(query: str = std_deviation) -> List[Dict]:
    conn = engine.connect()
    try:
        std_devs = conn.execute(query)
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