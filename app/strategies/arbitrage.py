from time import time

from app.core.models import Opportunity, Ticker


class ArbitrageStrategy:
    def __init__(self, min_spread_percent: float) -> None:
        self.min_spread_percent = min_spread_percent

    def check(self, ticker_a: Ticker, ticker_b: Ticker) -> Opportunity | None:
        opportunity_ab = self._check_direction(
            buy_ticker=ticker_a,
            sell_ticker=ticker_b,
        )

        if opportunity_ab:
            return opportunity_ab

        return self._check_direction(
            buy_ticker=ticker_b,
            sell_ticker=ticker_a,
        )

    def _check_direction(
        self,
        buy_ticker: Ticker,
        sell_ticker: Ticker,
    ) -> Opportunity | None:
        spread = sell_ticker.bid - buy_ticker.ask

        if spread <= 0:
            return None

        spread_percent = (spread / buy_ticker.ask) * 100

        if spread_percent < self.min_spread_percent:
            return None

        return Opportunity(
            symbol=buy_ticker.symbol,
            buy_exchange=buy_ticker.exchange,
            sell_exchange=sell_ticker.exchange,
            buy_price=buy_ticker.ask,
            sell_price=sell_ticker.bid,
            spread=spread,
            spread_percent=spread_percent,
            timestamp=time(),
        )
