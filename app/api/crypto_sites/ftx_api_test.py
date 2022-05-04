import asyncio

import aiohttp

from api.crypto_sites.binance_api import get_binance_coins_names
from app.api.crypto_sites.base_classes import CryptoSiteApi
from models.domain.users import Exchange


class FTX(CryptoSiteApi):
    name = "ftx"

    async def get_coin_price_from_api(self, name: str):
        res = []
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://ftx.com/api/markets/"
                async with session.get(url + f"{name}/USDT") as response:
                    json = await response.json()
                    result = json["result"]
                    coin_info = {"name": name, "price": result["price"]}
                    res.append(coin_info)
                    return coin_info
        except Exception:
            return None

    async def _get_coin_prices_from_api(self):
        names = get_binance_coins_names()  # We should get it from db
        tasks = []
        for name in names:
            task = self.get_coin_price_from_api(name)
            tasks.append(task)
        return await asyncio.gather(*tasks)

    async def get_coin_prices_from_api(self):
        res = list(filter(None, await self._get_coin_prices_from_api()))

        return res

    def get_coin_prices_from_db(self):
        pass


async def main():
    names = get_binance_coins_names()
    ftx = FTX()

    print(await ftx.get_coin_prices_from_api())


if __name__ == "__main__":
    asyncio.run(main())
