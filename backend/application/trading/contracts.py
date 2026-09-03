from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from application.trading.engine import TradingEngineResult

@dataclass(frozen=True, slots=True)
class TradingEngineInput:
    symbol: str
    realized_daily_pnl: float = 0.0
    unrealized_daily_pnl: float = 0.0

@dataclass(frozen=True, slots=True)
class TradingPipelineRequest:
    engine_input: TradingEngineInput
    portfolio_context: object

@dataclass(frozen=True, slots=True)
class TradingPipelineResult:
    run_id: str
    decision_id: str
    analysis: dict
    executed: bool
    order_id: str | None

class TradingPipelinePort(Protocol):
    async def run(self, run_id: str, request: TradingPipelineRequest, client_order_id: str) -> TradingPipelineResult: ...
