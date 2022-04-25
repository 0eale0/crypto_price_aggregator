from coinbase.wallet.client import Client
# import requests
from binance_api import binance_cryptocurrencies_usdt_price


def cryptocurrencies_usdt_price():
    # bubble_api_json_url = "https://cryptobubbles.net/backend/data/bubbles1000.usd.json"
    coinbase_API_key = '2310924'
    coinbase_API_secret = '49645645049'
    client = Client(coinbase_API_key, coinbase_API_secret)
    dict_crypto_price = dict()
    lst_crypto_name = []
    # response = requests.get(bubble_api_json_url)
    # crypto_json_name = response.json()
    result = binance_cryptocurrencies_usdt_price()
    for i in range(len(result)):
        lst_crypto_name.append(result[i]["symbol"][:-4])
    # print(lst_crypto_name)
    for i in lst_crypto_name:
        try:
            # print(client.get_exchange_rates(currency=i))
            dict_crypto_price[i] = client.get_exchange_rates(currency=i)["rates"]["USDT"]
        except:
            continue
    return dict_crypto_price


print(cryptocurrencies_usdt_price())
