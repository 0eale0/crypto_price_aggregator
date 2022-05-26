from app.api.crypto_sites.base_classes import CryptoSiteApi
import aiohttp
import asyncio


class BinanceAPI(CryptoSiteApi):
    name = "binance"

    async def get_coin_price_from_api(
        self, symbol: str
    ) -> dict[str, str | float] | None:  # pragma: no cover
        """
        It connects to binance_api and receives json,
        from which it extracts information about each coin (symbol and price)
        and writes it to a dictionary,
        which it then returns.
        Terminates the function in case of an error.
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.binance.com/"
                async with session.get(
                    url + f"api/v3/ticker/price?symbol={symbol.upper()}USDT"
                ) as response:
                    payload = await response.json()
                    coin_info = {"symbol": symbol, "price": float(payload["price"])}
                    return coin_info
        except Exception:
            return


async def main():  # pragma: no cover
    binance = BinanceAPI()
    return await binance.get_coin_prices_from_api()


if __name__ == "__main__":
    print((asyncio.run(main())))
