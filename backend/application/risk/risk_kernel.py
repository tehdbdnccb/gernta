from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RiskCheck:
    name: str
    passed: bool
    actual: float
    limit: float
    message: str

@dataclass(frozen=True, slots=True)
class RiskEvaluation:
    approved: bool
    checks: tuple[RiskCheck, ...]
    rejection_reasons: tuple[str, ...]

class DeterministicRiskKernel:
    MAX_TRADE_LOSS_PCT = 0.01
    MAX_DAILY_LOSS_PCT = 0.02
    MAX_OPEN_RISK_PCT = 0.05
    MAX_UNDERLYING_EXPOSURE_PCT = 0.02

    def evaluate(self, nav: float, trade_loss: float, daily_pnl: float, open_risk: float, underlying_exposure: float) -> RiskEvaluation:
        nav = max(nav, 0.0)
        checks = (
            self._check("trade_loss", trade_loss / nav if nav else 1.0, self.MAX_TRADE_LOSS_PCT, "Maximum trade loss"),
            self._check("daily_loss", max(-daily_pnl, 0.0) / nav if nav else 1.0, self.MAX_DAILY_LOSS_PCT, "Maximum daily loss"),
            self._check("open_risk", open_risk / nav if nav else 1.0, self.MAX_OPEN_RISK_PCT, "Maximum open risk"),
            self._check("underlying_exposure", underlying_exposure / nav if nav else 1.0, self.MAX_UNDERLYING_EXPOSURE_PCT, "Maximum underlying exposure"),
        )
        failures = tuple(c.message for c in checks if not c.passed)
        return RiskEvaluation(not failures, checks, failures)

    @staticmethod
    def _check(name: str, actual: float, limit: float, label: str) -> RiskCheck:
        return RiskCheck(name, actual <= limit, actual, limit, f"{label} exceeded" if actual > limit else f"{label} within limit")
