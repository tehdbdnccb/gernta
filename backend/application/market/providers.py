from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from application.market.features import MarketFeatures

class MarketDataProvider(Protocol):
    async def get_features(self, symbol: str) -> MarketFeatures: ...

@dataclass(slots=True)
class AlpacaMarketDataProvider:
    client: object

    async def get_features(self, symbol: str) -> MarketFeatures:
        # Deliberately conservative adapter: the trading pipeline can be wired to
        # historical/bar services without coupling domain logic to the SDK.
        quote = await self.client.get_latest_quote(symbol)
        price = float(quote["price"])
        return MarketFeatures(price=price, trend_pct=0.0, volatility_pct=0.0, momentum_pct=0.0)
