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

recommendations = (
    "select"
    " c.symbol, avg(cp.price) price"
                   " from coin_price cp"
                   " join cryptocurrencies c on c.id = cp.coin_id"
                   " where current_date - cp.time <= interval '5 minutes' and cp.price<="
                   " group by c.symbol"
                   " order by price desc"
)

# отклонение цены от среднего значения(средняя по всем биржами)
std_deviation = (
    "select"
    " c.symbol, date(cp.time) date, avg(cp.price) avg_price, stddev(cp.price) std_dev"
    " from coin_price cp"
    " left join cryptocurrencies c on c.id = cp.coin_id"
    " group by cp.coin_id, c.symbol, date"
    " order by cp.coin_id"
)
