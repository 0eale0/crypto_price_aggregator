import aiohttp


async def get_coin_description(coin_name: str) -> str | None:
    """
    Asks coingecko_api for json.
    From this json gets information about the cryptocurrency,
    the name of which is fed to the input of the function, and returns it.
    In case of an error that occurs if there is no information about the cryptocurrency in the api, it returns None.
    """
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
