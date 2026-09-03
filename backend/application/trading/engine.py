from __future__ import annotations
from dataclasses import dataclass, asdict
from application.ai.context import AIResearchContext
from application.ai.service import AIResearchService
from application.market.providers import MarketDataProvider
from application.market.regime import RegimeDetector
from application.quant.scorer import QuantScorer
from application.options.chain import OptionChainService
from application.options.strategy import DefinedRiskStrategy
from application.risk.risk_kernel import DeterministicRiskKernel
from application.trading.contracts import TradingEngineInput

@dataclass(frozen=True, slots=True)
class TradingEngineResult:
    analysis: dict
    candidate: object | None
    risk: object
    quant: object
    regime: object
    ai_thesis: object | None

class TradingEngine:
    def __init__(self, market: MarketDataProvider, regimes: RegimeDetector, ai: AIResearchService, quant: QuantScorer, chains: OptionChainService, strategy: DefinedRiskStrategy, risk: DeterministicRiskKernel):
        self.market, self.regimes, self.ai, self.quant, self.chains, self.strategy, self.risk = market, regimes, ai, quant, chains, strategy, risk

    async def analyze(self, request: TradingEngineInput, portfolio) -> TradingEngineResult:
        features = await self.market.get_features(request.symbol)
        regime = self.regimes.detect(features)
        ai_thesis = await self.ai.research(AIResearchContext.build(request.symbol, features, regime))
        confidence = ai_thesis.confidence if ai_thesis else regime.confidence
        quant = self.quant.score(regime, confidence)
        chain = await self.chains.get(request.symbol)
        candidate = self.strategy.build(regime.regime, chain, features.price)
        trade_loss = candidate.max_loss if candidate else portfolio.portfolio_value
        risk = self.risk.evaluate(portfolio.portfolio_value, trade_loss, request.realized_daily_pnl + request.unrealized_daily_pnl, portfolio.open_risk, portfolio.underlying_exposure)
        analysis = {"symbol":request.symbol,"features":asdict(features),"regime":asdict(regime),"ai_thesis":asdict(ai_thesis) if ai_thesis else None,"quant_score":asdict(quant),"option_candidate":asdict(candidate) if candidate else None,"risk":asdict(risk)}
        return TradingEngineResult(analysis, candidate, risk, quant, regime, ai_thesis)
