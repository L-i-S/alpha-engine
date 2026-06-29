import asyncio
import logging
from collections.abc import AsyncIterator

import aiohttp

from app.core.models import Ticker
from app.exchanges.base import BaseExchange

logger = logging.getLogger(__name__)


class BybitExchange(BaseExchange):
    name = "Bybit"
    rest_url = "https://api.bybit.com/v5/market/tickers"

    async def stream_ticker(self, symbol: str) -> AsyncIterator[Ticker]:
        logger.info("Starting Bybit REST ticker polling")

        async with aiohttp.ClientSession() as session:
            while True:
                params = {
                    "category": "spot",
                    "symbol": symbol,
                }

                async with session.get(
                    self.rest_url, params=params, timeout=10
                ) as response:
                    response.raise_for_status()
                    payload = await response.json()

                ticker_data = payload["result"]["list"][0]

                yield Ticker.from_bid_ask(
                    exchange=self.name,
                    symbol=symbol,
                    bid=float(ticker_data["bid1Price"]),
                    ask=float(ticker_data["ask1Price"]),
                )

                await asyncio.sleep(1)
