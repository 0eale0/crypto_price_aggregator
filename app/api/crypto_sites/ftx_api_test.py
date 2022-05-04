import asyncio

import aiohttp

from api.crypto_sites.binance_api import get_binance_coins_names
from app.api.crypto_sites.base_class import CryptoSiteApi


class FTX(CryptoSiteApi):
    async def get_coin_price(self, name: str):
        res = []
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://ftx.com/api/markets/'
                async with session.get(
                        url + f'{name}/USDT') as response:
                    json = await response.json()
                    result = json["result"]
                    coin_info = {"name": name, "price": result['price']}
                    res.append(coin_info)
                    return coin_info
        except Exception:
            return None

    async def __get_coin_prices(self):
        names = get_binance_coins_names()  # We should get it from db
        tasks = []
        for name in names:
            task = self.get_coin_price(name)
            tasks.append(task)
        return await asyncio.gather(*tasks)

    async def get_coin_prices(self):
        res = list(filter(None, await self.__get_coin_prices()))

        return res

    def save_in_db(self, result):
        pass


async def main():
    ftx = FTX()

    await ftx.get_coin_prices()


if __name__ == '__main__':
    asyncio.run(main())
