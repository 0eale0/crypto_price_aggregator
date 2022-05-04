from abc import ABC, abstractmethod


class CryptoSiteApi(ABC):
    @abstractmethod
    async def get_coin_price(self, name: str):
        pass

    @abstractmethod
    async def get_coin_prices(self):
        pass

    @abstractmethod
    async def save_in_db(self, result):
        pass
