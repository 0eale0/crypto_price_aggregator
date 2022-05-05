from api.crypto_sites.symbol_tracker import SymbolsTracker
from app.api.crypto_sites.base_class import CryptoSiteApi
import asyncio
import aiohttp
from pprint import pprint


class FTX(CryptoSiteApi):

    async def get_coin_price(self, symbol: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://ftx.com/api/markets/'
                async with session.get(
                        url + f'{symbol}/USDT') as response:
                    json = await response.json()
                    result = json["result"]
                    coin_info = {"symbol": symbol, "price": result['price']}
            return coin_info
        except Exception as e:
            return

    async def get_coin_prices(self):
        symbols = await SymbolsTracker.get_symbols()  # We should get it from db
        tasks = []
        for symbol in symbols:
            task = self.get_coin_price(symbol)
            tasks.append(task)

        solved_tasks = await asyncio.gather(*tasks)
        payload = list(filter(None, solved_tasks))
        return payload

    def save_in_db(self, result):
        pass


async def main():
    ftx = FTX()
    return await ftx.get_coin_prices()


if __name__ == '__main__':
    pprint((asyncio.run(main())))
