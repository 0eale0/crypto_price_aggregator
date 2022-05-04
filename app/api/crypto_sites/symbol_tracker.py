import aiohttp


class SymbolsTracker:
    """
    Gets all coins which represented in Binance, FTX, Kucoin
    """
    @staticmethod
    async def get_symbols():
        async with aiohttp.ClientSession() as session:
            url = "https://cryptobubbles.net/backend/data/bubbles1000.usd.json"
            async with session.get(url) as response:
                payload = await response.json()
                return [coin["symbol"] for coin in payload if
                        all([
                            coin["binanceSymbol"],
                            coin["ftxSymbol"],
                            coin["kucoinSymbol"]
                        ])]
