from binance_api import get_binance_coins_names
import aiohttp
import asyncio
import time


async def kucoin_prices(name: str):
    start = time.time()
    """
    Возвращает список монет с их именем и ценой, которые есть и на kucoin, и на binance
    """
    res = []
    try:
        async with aiohttp.ClientSession() as session:
            url = 'https://api.kucoin.com'
            async with session.get(
                    url + f'/api/v1/market/orderbook/level1?symbol={name}-USDT') as response:
                json = await response.json()
                data = json["data"]
                coin_info = {"name": name, "price": data['price']}
                res.append(coin_info)
                return coin_info
    except Exception:
        return None



async def main():
    names = get_binance_coins_names()
    tasks = []
    for name in names:
        task = kucoin_prices(name)
        tasks.append(task)
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    res = list(filter(None, loop.run_until_complete(main())))
    print(res)
    loop.close()
