min_max_price_for_each = ("select coin_id, max(price), min(price)"
       "from coin_price"
       " where current_date - coin_price.time <= interval '5 minutes'"
       "group by coin_id order by coin_id")