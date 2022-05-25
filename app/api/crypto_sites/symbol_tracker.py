import asyncio
from pprint import pprint
from typing import List, Dict

import aiohttp

from app.api.services.api_config import symbols_for_tracker


class SymbolsTracker:
    symbols = symbols_for_tracker

    async def get_symbols(self) -> List[Dict]:
        """
        Refers to the cryptobubbles_api,
        creates a list of dictionaries with the names of the coins
        that are in kucoin_api, ftx api, binance api,
        cryptobubbles_api and their symbols.
        """
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
