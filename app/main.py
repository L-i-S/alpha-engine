import logging

from app.config.settings import settings
from app.core.logging import setup_logging
from app.core.models import Ticker
from app.strategies.arbitrage import ArbitrageStrategy

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging(settings.log_level)

    strategy = ArbitrageStrategy(settings.min_spread_percent)

    binance = Ticker.from_bid_ask(
        exchange="Binance",
        symbol="BTCUSDT",
        bid=100100,
        ask=100110,
    )

    bybit = Ticker.from_bid_ask(
        exchange="Bybit",
        symbol="BTCUSDT",
        bid=100500,
        ask=100510,
    )

    opportunity = strategy.check(binance, bybit)

    if opportunity:
        logger.info("Opportunity found:")
        logger.info(opportunity)
    else:
        logger.info("No opportunity")


if __name__ == "__main__":
    main()
