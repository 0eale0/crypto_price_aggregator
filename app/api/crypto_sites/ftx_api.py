from binance_api import binance_cryptocurrencies_usdt_price, get_binance_coins_names
import aiohttp
import asyncio
import time


async def cryptocurrencies_usdt_price(name: str):
    start = time.time()
    """
    Возвращает список монет с их именем и ценой, которые есть и на ftx, и на binance
    """
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


async def main():
    names = get_binance_coins_names()
    tasks = []
    for name in names:
        task = cryptocurrencies_usdt_price(name)
        tasks.append(task)
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    res = list(filter(None, loop.run_until_complete(main())))
    print(res)
    loop.close()

