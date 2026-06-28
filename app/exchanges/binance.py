import json
import logging
from collections.abc import AsyncIterator

import websockets

from app.core.models import Ticker
from app.exchanges.base import BaseExchange

logger = logging.getLogger(__name__)


class BinanceExchange(BaseExchange):
    name = "Binance"
    ws_base_url = "wss://stream.binance.com:9443/ws"

    async def stream_ticker(self, symbol: str) -> AsyncIterator[Ticker]:
        stream_symbol = symbol.lower()
        url = f"{self.ws_base_url}/{stream_symbol}@bookTicker"

        logger.info("Connecting to Binance WebSocket: %s", url)

        async with websockets.connect(url) as websocket:
            async for message in websocket:
                data = json.loads(message)

                yield Ticker.from_bid_ask(
                    exchange=self.name,
                    symbol=symbol,
                    bid=float(data["b"]),
                    ask=float(data["a"]),
                )
