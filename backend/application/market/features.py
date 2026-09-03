from __future__ import annotations
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True, slots=True)
class MarketFeatures:
    price: float
    trend_pct: float
    volatility_pct: float
    momentum_pct: float

    def validate(self) -> None:
        if self.price <= 0 or not all(isfinite(x) for x in (self.price, self.trend_pct, self.volatility_pct, self.momentum_pct)):
            raise ValueError("Invalid market features")
