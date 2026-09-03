from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from application.market.features import MarketFeatures

MarketRegime = Literal["bullish", "bearish", "neutral", "high_volatility"]

@dataclass(frozen=True, slots=True)
class RegimeResult:
    regime: MarketRegime
    confidence: float
    rationale: str

class RegimeDetector:
    def detect(self, features: MarketFeatures) -> RegimeResult:
        features.validate()
        if features.volatility_pct >= 4.0:
            return RegimeResult("high_volatility", min(features.volatility_pct / 8.0, 1.0), "Volatility exceeds execution threshold.")
        score = 0.6 * features.trend_pct + 0.4 * features.momentum_pct
        if score >= 1.0:
            return RegimeResult("bullish", min(0.5 + abs(score) / 10, 0.99), "Trend and momentum are aligned upward.")
        if score <= -1.0:
            return RegimeResult("bearish", min(0.5 + abs(score) / 10, 0.99), "Trend and momentum are aligned downward.")
        return RegimeResult("neutral", max(0.5 - abs(score) / 10, 0.2), "Trend and momentum are not sufficiently aligned.")
