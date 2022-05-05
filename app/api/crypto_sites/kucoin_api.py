from app.api.crypto_sites.base_class import CryptoSiteApi
import aiohttp
import asyncio
from pprint import pprint


class KucoinAPI(CryptoSiteApi):
    async def get_coin_price(self, symbol: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://api.kucoin.com'
                async with session.get(
                        url + f'/api/v1/market/orderbook/level1?symbol={symbol.upper()}-USDT') as response:
                    json = await response.json()
                    data = json["data"]
                    coin_info = {"name": symbol.upper(), "price": float(data['price'])}
                    return coin_info
        except Exception:
            return

    def save_in_db(self, result):
        pass


async def main():
    kucoin = KucoinAPI()
    return await kucoin.get_coin_prices()


if __name__ == '__main__':
    pprint((asyncio.run(main())))
