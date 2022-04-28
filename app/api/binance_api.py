from binance.client import Client


def binance_cryptocurrencies_usdt_price() -> list:
    """
    Возвращает отсортированные пары по цене в долларах от большего к меньшему
    """
    result = list()
    c = Client()
    tickers = c.get_all_tickers()
    for coin in tickers:
        coin["price"] = float(coin["price"])
        if "USDT" in coin['symbol']:
            result.append(coin)
        else:
            continue
    return list(filter(lambda x: max(str(x['price'])), result))


def get_binance_coins_names():
    names = []
    result = binance_cryptocurrencies_usdt_price()
    for coin in result:
        names.append(coin["symbol"][:-4])
    return names

# print(get_binance_coins_names())
# print(binance_cryptocurrencies_usdt_price())
