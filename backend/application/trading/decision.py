from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from application.risk.risk_kernel import RiskEvaluation
from application.quant.scorer import QuantScore

@dataclass(frozen=True, slots=True)
class TradingDecision:
    id: str
    approved: bool
    reasons: tuple[str, ...]

class DecisionService:
    def decide(self, quant: QuantScore, risk: RiskEvaluation) -> TradingDecision:
        reasons = list(risk.rejection_reasons)
        if quant.total < 60: reasons.append("Quant score below approval threshold")
        return TradingDecision(str(uuid4()), not reasons, tuple(reasons))
