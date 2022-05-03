from app.api.crypto_sites.ftx_api_test import FTX
from app.api.crypto_sites.base_classes import CryptoSitesApi

ftx = FTX()
crypto_sites = [ftx]
crypto_api = CryptoSitesApi(list_with_api=crypto_sites)
