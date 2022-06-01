from app.api.crypto_sites.base_classes import CryptoSiteApi
import aiohttp
import asyncio
from pprint import pprint
from typing import Union, Dict


class KucoinAPI(CryptoSiteApi):  # pragma: no cover
    name = "kucoin"

    async def get_coin_price_from_api(
        self, symbol: str
    ) -> Union[Dict[str, float], None]:
        """
        Connects to kucoin_api and gets json,
        from which receives information about each coin (symbol and price)
        and writes to a dictionary, which is then returned.
        In case of an error, it terminates the function.
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.kucoin.com"
                async with session.get(
                    url
                    + f"/api/v1/market/orderbook/level1?symbol={symbol.upper()}-USDT", ssl=False
                ) as response:
                    json = await response.json()
                    data = json["data"]
                    coin_info = {
                        "symbol": symbol.upper(),
                        "price": float(data["price"]),
                    }
                    return coin_info
        except Exception as error:
            print(error)
            return


async def main():  # pragma: no cover
    kucoin = KucoinAPI()
    return await kucoin.get_coin_prices_from_api()


if __name__ == "__main__":  # pragma: no cover
    pprint((asyncio.run(main())))  # pragma: no cover
