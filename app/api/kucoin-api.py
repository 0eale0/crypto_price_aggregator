import requests
import json
import datetime
from binance_api import binance_cryptocurrencies_usdt_price


def kucoin_cryptocurrencies_usdt_price():
    dict_crypto_price = dict()
    lst_crypto_name = []
    url = 'https://api.kucoin.com'
    # response = requests.get(bubble_api_json_url)
    # crypto_json_name = response.json()
    result = binance_cryptocurrencies_usdt_price()
    for i in range(len(result)):
        lst_crypto_name.append(result[i]["symbol"][:-4])
    for i in lst_crypto_name:
        try:
            # print(client.get_exchange_rates(currency=i))
            dict_crypto_price[i] = \
            requests.get(url + f'/api/v1/market/orderbook/level1?symbol={i}' + '-USDT').json()["data"]["price"]
        except:
            continue
    return dict_crypto_price


print(kucoin_cryptocurrencies_usdt_price())
