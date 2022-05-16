"""
Просьба не трогать
"""

min_max_average_price_by_exchange_for_each = (
    "select"
    " cp.coin_id, c.symbol, cp.exchange_id, max(price), min(price), avg(price)"
    " from coin_price cp"
    " join cryptocurrencies c on c.id = cp.coin_id"
    " where current_date - cp.time <= interval '1 day'"
    " group by c.symbol, cp.coin_id, cp.exchange_id"
    " order by cp.coin_id"
)
