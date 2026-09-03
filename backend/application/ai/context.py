from __future__ import annotations
from dataclasses import asdict
from application.ai.thesis import AIThesis
from application.market.features import MarketFeatures
from application.market.regime import RegimeResult

class AIResearchContext:
    @staticmethod
    def build(symbol: str, features: MarketFeatures, regime: RegimeResult) -> dict:
        return {"symbol": symbol, "features": asdict(features), "regime": asdict(regime)}
