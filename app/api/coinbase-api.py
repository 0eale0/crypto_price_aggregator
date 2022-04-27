from binance_api import binance_cryptocurrencies_usdt_price, get_binance_coins_names
import aiohttp
import asyncio
import time


async def cryptocurrencies_usdt_price(name: str):
    start = time.time()
    """
    Возвращает список монет с их именем и ценой, которые есть и на coinbase, и на binance
    """
    res = []
    try:
        async with aiohttp.ClientSession() as session:
            url = 'https://api.exchange.coinbase.com/products/'
            async with session.get(
                    url + f'{name}-USDT/ticker') as response:
                json = await response.json()
                coin_info = {"name": name, "price": json['price']}
                res.append(coin_info)
                return coin_info
    except Exception:
        return name


async def main():
    names = get_binance_coins_names()
    tasks = []
    for name in names:
        task = cryptocurrencies_usdt_price(name)
        tasks.append(task)
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    print(asyncio.run(main()))
