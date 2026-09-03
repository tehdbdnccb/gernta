from __future__ import annotations
from dataclasses import dataclass
from application.market.regime import RegimeResult

@dataclass(frozen=True, slots=True)
class QuantContribution:
    factor: str
    score: float
    weight: float

@dataclass(frozen=True, slots=True)
class QuantScore:
    total: float
    contributions: tuple[QuantContribution, ...]
    label: str

class QuantScorer:
    def score(self, regime: RegimeResult, ai_confidence: float = 0.5) -> QuantScore:
        regime_score = {"bullish": 80.0, "bearish": 80.0, "neutral": 40.0, "high_volatility": 20.0}[regime.regime]
        confidence_score = max(0.0, min(ai_confidence, 1.0)) * 100
        total = 0.75 * regime_score + 0.25 * confidence_score
        label = "STRONG" if total >= 75 else "VALID" if total >= 60 else "WEAK"
        return QuantScore(total, (QuantContribution("regime", regime_score, .75), QuantContribution("research_confidence", confidence_score, .25)), label)
