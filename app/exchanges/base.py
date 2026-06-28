from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.core.models import Ticker


class BaseExchange(ABC):
    name: str

    @abstractmethod
    async def stream_ticker(self, symbol: str) -> AsyncIterator[Ticker]:
        """Stream best bid/ask ticker data for a symbol."""
        raise NotImplementedError
