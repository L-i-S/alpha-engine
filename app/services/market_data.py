import asyncio
import logging

from app.core.models import Ticker
from app.exchanges.base import BaseExchange

logger = logging.getLogger(__name__)


class MarketDataService:
    def __init__(self, exchanges: list[BaseExchange], symbol: str) -> None:
        self.exchanges = exchanges
        self.symbol = symbol
        self.latest_tickers: dict[str, Ticker] = {}

    async def start(self) -> None:
        tasks = [
            asyncio.create_task(self._stream_exchange(exchange))
            for exchange in self.exchanges
        ]

        await asyncio.gather(*tasks)

    async def _stream_exchange(self, exchange: BaseExchange) -> None:
        async for ticker in exchange.stream_ticker(self.symbol):
            self.latest_tickers[ticker.exchange] = ticker
            logger.debug("Updated ticker: %s", ticker)

    def get_latest_tickers(self) -> list[Ticker]:
        return list(self.latest_tickers.values())
