from app.api.crypto_sites.base_classes import CryptoSiteApi
import asyncio
import aiohttp
from pprint import pprint


class FTXApi(CryptoSiteApi):

    name = "ftx"

    async def get_coin_price_from_api(self, symbol: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://ftx.com/api/markets/"
                async with session.get(url + f"{symbol}/USDT") as response:
                    json = await response.json()
                    result = json["result"]
                    coin_info = {"symbol": symbol, "price": result["price"]}
            return coin_info
        except Exception as e:
            return


async def main():
    ftx = FTXApi()
    return await ftx.get_coin_prices_from_api()


if __name__ == "__main__":
    pprint((asyncio.run(main())))
