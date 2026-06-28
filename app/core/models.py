from dataclasses import dataclass
from enum import Enum
from time import time


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass(frozen=True)
class Ticker:
    exchange: str
    symbol: str
    bid: float
    ask: float
    timestamp: float

    @classmethod
    def from_bid_ask(
        cls,
        exchange: str,
        symbol: str,
        bid: float,
        ask: float,
    ) -> "Ticker":
        return cls(
            exchange=exchange,
            symbol=symbol,
            bid=bid,
            ask=ask,
            timestamp=time(),
        )


@dataclass(frozen=True)
class Opportunity:
    symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    spread: float
    spread_percent: float
    timestamp: float


@dataclass(frozen=True)
class Order:
    exchange: str
    symbol: str
    side: OrderSide
    amount: float
    price: float


@dataclass(frozen=True)
class TradeResult:
    exchange: str
    symbol: str
    side: OrderSide
    amount: float
    price: float
    success: bool
    message: str


@dataclass(frozen=True)
class Balance:
    exchange: str
    asset: str
    free: float
    locked: float
