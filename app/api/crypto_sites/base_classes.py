import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.api.crypto_sites.coingecko_api import get_coin_description
from app.api.crypto_sites.symbol_tracker import SymbolsTracker
from app.models.domain import users
from app.models.domain.users import Exchange, Cryptocurrency, CoinPrice


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
    def save_price_in_db(self, result):
        pass

    @abstractmethod
    def init_coins_in_db(self, coin):
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
        coins_info = await SymbolsTracker().get_symbols()  # We should get it from db
        tasks = []
        for coin_info in coins_info:
            task = self.get_coin_price_from_api(coin_info["symbol"])
            tasks.append(task)

        solved_tasks = await asyncio.gather(*tasks)
        payload = list(filter(None, solved_tasks))
        return payload

    def get_coin_price_from_db(self, name: str):
        pass

    # TODO MAKE IT WITHOUT DUMPS
    def get_coin_prices_from_db(self):
        session = users.session()
        exchange_id = session.query(Exchange).filter_by(name=self.name).one().id

        max_time_from_db = session.query(func.max(users.CoinPrice.time)) \
            .filter_by(exchange_id=exchange_id) \
            .first()[0]

        coins_and_prices_from_db = session.query(users.Cryptocurrency, users.CoinPrice) \
            .join(users.Cryptocurrency) \
            .order_by(users.CoinPrice.time).filter(users.CoinPrice.time == max_time_from_db)

        result = []

        for coin in coins_and_prices_from_db:
            coin_info = {"symbol": coin[0].symbol, "name": coin[0].name,
                         "price": coin[1].price}
            result.append(coin_info)
        return result

    def save_price_in_db(self, result):
        # add coins into db, if it's not
        model_crypto = users.Cryptocurrency
        session = users.session()
        time_for_coin = datetime.now(timezone.utc)
        with session as sess:
            for coin in result:
                coin_id = sess.query(Cryptocurrency).filter_by(symbol=coin["symbol"]).first().id
                exchange_id = session.query(Exchange).filter_by(name=self.name).one().id
                price = coin["price"]

                coin_price_with_time = users.CoinPrice(coin_id=coin_id, exchange_id=exchange_id,
                                                       price=price, time=time_for_coin)

                sess.add(coin_price_with_time)

                sess.commit()

    async def init_coins_in_db(self, coins):
        session = users.session()

        with session as sess:
            for coin in coins:
                coin_from_db = sess.query(Cryptocurrency).filter_by(symbol=coin["symbol"]).first()
                if not coin_from_db:
                    coin["name"] = coin["name"].lower()
                    coin_description = await get_coin_description(coin["name"])
                    coin["crypto_info"] = coin_description

                    values_to_write_into_cryptocurrency_db = ["symbol", "name", "crypto_info"]
                    info_for_write_into_cryptocurrency_db = {key: coin[key] for key in
                                                             values_to_write_into_cryptocurrency_db}

                    crypto_currency = users.Cryptocurrency(**info_for_write_into_cryptocurrency_db)
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
            coins_info = await SymbolsTracker().get_symbols()
            prices_from_api = await api.get_coin_prices_from_api()

            await api.init_coins_in_db(coins_info)
            api.save_price_in_db(prices_from_api)

    # TODO END IT
    def get_coin_prices(self):
        result = {}
        for api in self.list_with_api:
            result[api.name] = api.get_coin_prices_from_db()

        return result
