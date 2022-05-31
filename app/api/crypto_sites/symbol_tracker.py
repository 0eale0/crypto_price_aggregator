import asyncio
from pprint import pprint
import aiohttp
from typing import Dict, List
from app.api.services.api_config import symbols_for_tracker


class SymbolsTracker:  # pragma: no cover
    symbols = symbols_for_tracker

    async def get_symbols(self) -> List[Dict[str, str]]:
        """
        Refers to the CryptobubblesApi and
        creates a list of dictionaries with the names of the coins
        that are in kucoin_api, ftx api, binance api,
        cryptobubbles_api and their symbols.
        """
        async with aiohttp.ClientSession() as session:
            url = "https://cryptobubbles.net/backend/data/bubbles1000.usd.json"
            async with session.get(url, ssl=False) as response:
                payload = await response.json()
                return [
                    {"symbol": coin["symbol"], "name": coin["name"]}
                    for coin in payload
                    if all([coin[symbol] for symbol in self.symbols])
                ]


async def main():  # pragma: no cover
    tracker = SymbolsTracker()
    return await tracker.get_symbols()


if __name__ == "__main__":  # pragma: no cover
    pprint((asyncio.run(main())))  # pragma: no cover
