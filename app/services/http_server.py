from aiohttp import web
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.services.market_data import MarketDataService


async def healthz(_: web.Request) -> web.Response:
    return web.Response(text="OK")


async def readyz(request: web.Request) -> web.Response:
    market: MarketDataService = request.app["market"]

    if len(market.get_latest_tickers()) >= 2:
        return web.Response(text="READY")

    return web.Response(status=503, text="NOT READY")


async def metrics(_: web.Request) -> web.Response:
    return web.Response(
        body=generate_latest(),
        headers={"Content-Type": CONTENT_TYPE_LATEST},
    )


def create_app(market: MarketDataService) -> web.Application:
    app = web.Application()
    app["market"] = market

    app.router.add_get("/healthz", healthz)
    app.router.add_get("/readyz", readyz)
    app.router.add_get("/metrics", metrics)

    return app
