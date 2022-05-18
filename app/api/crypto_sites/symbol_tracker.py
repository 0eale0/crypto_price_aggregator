import asyncio
from pprint import pprint

import aiohttp

from app.api.services.api_config import symbols_for_tracker


class SymbolsTracker:
    symbols = symbols_for_tracker
    """
    Gets all coins which represented in Binance, FTX, Kucoin
    """

    async def get_symbols(self):
        async with aiohttp.ClientSession() as session:
            url = "https://cryptobubbles.net/backend/data/bubbles1000.usd.json"
            async with session.get(url) as response:
                payload = await response.json()
                return [
                    {"symbol": coin["symbol"], "name": coin["name"]}
                    for coin in payload
                    if all([coin[symbol] for symbol in self.symbols])
                ]


async def main():
    tracker = SymbolsTracker()
    return await tracker.get_symbols()


if __name__ == "__main__":
    pprint((asyncio.run(main())))
