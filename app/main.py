import asyncio
import logging

from app.config.settings import settings
from app.core.logging import setup_logging
from app.exchanges.binance import BinanceExchange

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging(settings.log_level)

    exchange = BinanceExchange()

    async for ticker in exchange.stream_ticker(settings.symbol):
        logger.info(ticker)


if __name__ == "__main__":
    asyncio.run(main())
