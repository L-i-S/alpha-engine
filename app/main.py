import asyncio
import logging

from aiohttp import web

from app.config.settings import settings
from app.core.logging import setup_logging
from app.exchanges.binance import BinanceExchange
from app.exchanges.bybit import BybitExchange
from app.services.http_server import create_app
from app.services.market_data import MarketDataService
from app.strategies.arbitrage import ArbitrageStrategy

logger = logging.getLogger(__name__)


async def start_http_server(market: MarketDataService) -> None:
    app = create_app(market)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host=settings.http_host,
        port=settings.http_port,
    )

    await site.start()

    logger.info(
        "HTTP server started on %s:%s",
        settings.http_host,
        settings.http_port,
    )

    while True:
        await asyncio.sleep(3600)


async def check_opportunities(market: MarketDataService) -> None:
    strategy = ArbitrageStrategy(settings.min_spread_percent)

    while True:
        await asyncio.sleep(5)

        tickers = market.get_latest_tickers()

        if len(tickers) < 2:
            logger.info("Waiting for market data... received=%s", len(tickers))
            continue

        ticker_a = tickers[0]
        ticker_b = tickers[1]

        logger.info(
            "Market data: %s bid=%s ask=%s | %s bid=%s ask=%s",
            ticker_a.exchange,
            ticker_a.bid,
            ticker_a.ask,
            ticker_b.exchange,
            ticker_b.bid,
            ticker_b.ask,
        )

        opportunity = strategy.check(ticker_a, ticker_b)

        if opportunity:
            logger.info("========== OPPORTUNITY ==========")
            logger.info(opportunity)
        else:
            logger.info(
                "No opportunity above threshold: %s%%",
                settings.min_spread_percent,
            )


async def main() -> None:
    setup_logging(settings.log_level)

    logger.info("Alpha Engine started")
    logger.info("Symbol: %s", settings.symbol)
    logger.info("Min spread: %s%%", settings.min_spread_percent)

    market = MarketDataService(
        exchanges=[
            BinanceExchange(),
            BybitExchange(),
        ],
        symbol=settings.symbol,
    )

    await asyncio.gather(
        market.start(),
        check_opportunities(market),
        start_http_server(market),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Alpha Engine stopped")
