from app.api.crypto_sites.ftx_api import FTXApi
from app.api.crypto_sites.base_classes import CryptoSitesApi

ftx = FTXApi()
crypto_sites = [ftx]
crypto_api = CryptoSitesApi(list_with_api=crypto_sites)
