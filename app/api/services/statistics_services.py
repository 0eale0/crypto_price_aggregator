from app.models.domain.users import engine
from typing import List, Dict


def get_aggregated_prices(query: str) -> List[Dict]:
    conn = engine.connect()
    try:
        aggregated_prices = conn.execute(query)
        return [r for r in aggregated_prices]
    except Exception as e:
        return e