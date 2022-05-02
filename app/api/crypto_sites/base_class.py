from abc import ABC, abstractmethod


class CryptoSiteApi(ABC):
    @abstractmethod
    def get_coin_price(self, name: str):
        pass

    @abstractmethod
    def __get_coin_prices(self):
        pass

    @abstractmethod
    def get_coin_prices(self):
        pass

    @abstractmethod
    def save_in_db(self, result):
        pass
