import aiohttp


async def get_coin_description(coin_name):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"https://api.coingecko.com/api/v3/coins/{coin_name}"
            ) as response:
                json = await response.json()
                coin_info = json["description"]["en"]
        except Exception:
            coin_info = None

        return coin_info
