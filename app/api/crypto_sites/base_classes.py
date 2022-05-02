from abc import ABC, abstractmethod


class CryptoSiteApi(ABC):
    site_name = "name"

    @abstractmethod
    def get_coin_price_from_api(self, name: str):
        pass

    @abstractmethod
    def __get_coin_prices_from_api(self):
        pass

    @abstractmethod
    def get_coin_prices_from_api(self):
        pass

    @abstractmethod
    def save_in_db(self, result):
        pass

    @abstractmethod
    def get_coin_prices_from_db(self):
        pass


class CryptoSitesApi(ABC):
    def __init__(self, list_with_api: list):
        self.list_with_api = list_with_api

    async def update_coin_prices(self):
        for api in self.list_with_api:
            prices_from_api = await api.get_coin_prices_from_api()
            api.save_in_db(prices_from_api)

    # TODO there is should be work with db ang get info from it
    def get_coin_prices(self):
        pass
