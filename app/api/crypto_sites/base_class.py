import asyncio
from abc import ABC, abstractmethod

from api.crypto_sites.symbol_tracker import SymbolsTracker


class CryptoSiteApiInterface(ABC):
    @abstractmethod
    async def get_coin_price(self, name: str):
        pass

    @abstractmethod
    async def get_coin_prices(self):
        pass

    @abstractmethod
    async def save_in_db(self, result):
        pass


class CryptoSiteApi(CryptoSiteApiInterface):
    async def get_coin_price(self, name: str):
        pass

    async def get_coin_prices(self):
        symbols = await SymbolsTracker.get_symbols()  # We should get it from db
        tasks = []
        for symbol in symbols:
            task = self.get_coin_price(symbol)
            tasks.append(task)

        solved_tasks = await asyncio.gather(*tasks)
        payload = list(filter(None, solved_tasks))
        return payload

    async def save_in_db(self, result):
        pass
