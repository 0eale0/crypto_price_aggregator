from app.api.crypto_sites.base_classes import CryptoSiteApi
import asyncio
import aiohttp
from pprint import pprint
from typing import Union, Dict


class FTXApi(CryptoSiteApi):  # pragma: no cover
    name = "ftx"

    async def get_coin_price_from_api(
        self, symbol: str
    ) -> Union[Dict[str, float], None]:
        """
        Requests ftx_api json.
        From this json gets information about the cryptocurrency (symbol and price),
        the name of which is fed to the input of the function,
        and returns it in the form of a dictionary.
        In case of an error, it terminates the function.
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://ftx.com/api/markets/"
                async with session.get(url + f"{symbol}/USDT") as response:
                    json = await response.json()
                    result = json["result"]
                    coin_info = {"symbol": symbol, "price": result["price"]}
            return coin_info
        except Exception:
            return


async def main():  # pragma: no cover
    ftx = FTXApi()
    return await ftx.get_coin_prices_from_api()


if __name__ == "__main__":
    pprint((asyncio.run(main())))  # pragma: no cover
