from app.api.crypto_sites.base_class import CryptoSiteApi
from app.api.crypto_sites.symbol_tracker import SymbolsTracker
import aiohttp
import asyncio


class BinanceAPI(CryptoSiteApi):

    async def get_coin_price(self, symbol: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://api.binance.com/'
                async with session.get(
                            url + f'api/v3/ticker/price?symbol={symbol.upper()}USDT') as response:
                        payload = await response.json()
                        return payload
                        coin_info = {"name": symbol, "price": float(payload['price'])}
                        return coin_info
        except Exception:
            return

    async def __get_coin_prices(self):
        symbols = await SymbolsTracker.get_symbols()  # We should get it from db
        tasks = []
        for symbol in symbols:
            task = self.get_coin_price(symbol)
            tasks.append(task)
        return await asyncio.gather(*tasks)

    async def get_coin_prices(self):
        payload = list(filter(None, await self.__get_coin_prices()))
        return payload

    async def save_in_db(self, result):
        pass


async def main():
    binance = BinanceAPI()
    return await binance.get_coin_price('btc')

if __name__ == '__main__':
        print((asyncio.run(main())))