import asyncio
from abc import ABC, abstractmethod

from sqlalchemy.exc import IntegrityError

from api.crypto_sites.symbol_tracker import SymbolsTracker
from models.domain import users
from models.domain.users import Exchange


class CryptoSiteApiInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def get_coin_price_from_api(self, name: str):
        pass

    @abstractmethod
    async def get_coin_prices_from_api(self):
        pass

    @abstractmethod
    def get_coin_price_from_db(self, name: str):
        pass

    @abstractmethod
    def get_coin_prices_from_db(self):
        pass

    @abstractmethod
    def save_in_db(self, result):
        pass


class CryptoSiteApi(CryptoSiteApiInterface):
    name = "null"

    # Create exchange in db if it's not
    def __init__(self):
        session = users.session()

        with session as sess:
            exchange = Exchange(name=self.name)
            sess.add(exchange)

            try:
                sess.commit()
            except IntegrityError:
                pass

    async def get_coin_price_from_api(self, name: str):
        pass

    async def get_coin_prices_from_api(self):
        symbols = await SymbolsTracker().get_symbols()  # We should get it from db
        tasks = []
        for symbol in symbols:
            task = self.get_coin_price_from_api(symbol)
            tasks.append(task)

        solved_tasks = await asyncio.gather(*tasks)
        payload = list(filter(None, solved_tasks))
        return payload

    def get_coin_price_from_db(self, name: str):
        pass

    # TODO MAKE IT WITHOUT DUMPS
    def get_coin_prices_from_db(self):
        model_crypto = users.Cryptocurrency
        session = users.session()
        exchange_id = session.query(Exchange).filter_by(name=self.name).one().id

        result = session.query(model_crypto).filter_by(exchange_id=exchange_id)
        result = [coin.dumps() for coin in result]

        return result

    # TODO FIX UPDATE IN DB
    def save_in_db(self, result):
        model_crypto = users.Cryptocurrency
        session = users.session()
        exchange_id = session.query(Exchange).filter_by(name=self.name).one().id
        with session as sess:
            for coin in result:
                coin["exchange_id"] = exchange_id
                crypto_currency = model_crypto(**coin)
                sess.add(crypto_currency)

            sess.commit()


class CryptoSitesApiInterface(ABC):
    def __init__(self, list_with_api: list):
        self.list_with_api = list_with_api

    @abstractmethod
    async def update_coin_prices_in_db(self):
        pass

    @abstractmethod
    def get_coin_prices(self):
        pass


class CryptoSitesApi(CryptoSitesApiInterface):
    def __init__(self, list_with_api: list):
        super().__init__(list_with_api)

    async def update_coin_prices_in_db(self):
        for api in self.list_with_api:
            prices_from_api = await api.get_coin_prices_from_api()
            api.save_in_db(prices_from_api)

    # TODO END IT
    def get_coin_prices(self):
        result = {}
        for api in self.list_with_api:
            result[api.name] = api.get_coin_prices_from_db()

        return result
