from binance.client import Client


def binance_cryptocurrencies_usdt_price() -> list:
    """
    Возвращает отсортированные пары по цене в долларах от большего к меньшему
    """
    result = list()
    c = Client()
    tickers = c.get_all_tickers()
    for coin in tickers:
        if "USDT" in coin['symbol']:
            result.append(coin)
        else:
            continue
    return list(filter(lambda x: max(x['price']), result))


# print(binance_cryptocurrencies_usdt_price())
