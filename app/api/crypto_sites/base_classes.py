from abc import ABC, abstractmethod

from models.domain import users
from models.domain.users import Exchange


class CryptoSiteApi(ABC):
    site_name = "name"

    @abstractmethod
    def get_coin_price_from_api(self, name: str):
        pass

    def init_in_db(self):
        pass

    @abstractmethod
    def _get_coin_prices_from_api(self):
        pass

    @abstractmethod
    def get_coin_prices_from_api(self):
        pass

    def save_in_db(self, result):
        model_crypto = users.Cryptocurrency
        session = users.session()

        exchange_id = session.query(Exchange).filter_by(name="ftx").one().id
        with session as sess:
            for coin in result:
                coin["exchange_id"] = exchange_id
                print(coin)
                crypto_currency = model_crypto(**coin)
                sess.add(crypto_currency)

            print("I AM DONE HEEEY")

            sess.commit()

            print("I AM COMMIT")

    @abstractmethod
    def get_coin_prices_from_db(self):
        pass


class CryptoSitesApi(ABC):
    def __init__(self, list_with_api: list):
        self.list_with_api = list_with_api

    async def update_coin_prices(self):
        for api in self.list_with_api:
            prices_from_api = await api.get_coin_prices_from_api()
            print(prices_from_api)
            api.save_in_db(prices_from_api)

    # TODO there is should be work with db ang get info from it
    def get_coin_prices(self):
        pass
