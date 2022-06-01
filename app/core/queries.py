"""
Просьба не трогать
"""

min_max_average_price_by_exchange_for_each = (
    "select"
    " cp.coin_id, c.symbol, e.name, max(price), min(price), avg(price)"
    " from coin_price cp"
    " join cryptocurrencies c on c.id = cp.coin_id"
    " join exchanges e on e.id = cp.exchange_id"
    " where current_date - cp.time <= interval '1 day'"
    " group by c.symbol, cp.coin_id, e.name"
    " order by cp.coin_id"
)


avg_prices_by_day = (
    "select"
    " c.symbol, avg(price) avg_price, date(time) as day"
    " from coin_price cp"
    " join cryptocurrencies c on c.id = cp.coin_id"
    " where symbol="
    " group by c.symbol, date(time)"
    " order by day"
)
