from api.crypto_sites.ftx_api import FTXApi
from api.crypto_sites.kucoin_api import KucoinAPI
from api.crypto_sites.binance_api import BinanceAPI
from api.crypto_sites.base_classes import CryptoSitesApi

ftx_api = FTXApi()
kucoin_api = KucoinAPI()
binance_api = BinanceAPI()

crypto_sites = [ftx_api, kucoin_api, binance_api]
crypto_api = CryptoSitesApi(list_with_api=crypto_sites)
