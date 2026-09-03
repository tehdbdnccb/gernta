from __future__ import annotations
from application.trading.contracts import TradingPipelinePort, TradingPipelineRequest, TradingPipelineResult
from application.trading.engine import TradingEngine
from application.trading.decision import DecisionService
from application.trading.execution import ExecutionService
from application.trading.journal import JournalService

class TradingPipeline(TradingPipelinePort):
    def __init__(self, engine: TradingEngine, decisions: DecisionService, execution: ExecutionService, journal: JournalService): self.engine,self.decisions,self.execution,self.journal=engine,decisions,execution,journal
    async def run(self, run_id: str, request: TradingPipelineRequest, client_order_id: str) -> TradingPipelineResult:
        result=await self.engine.analyze(request.engine_input, request.portfolio_context)
        decision=self.decisions.decide(result.quant,result.risk)
        executed=False; order_id=None
        if decision.approved and result.candidate:
            order=await self.execution.execute(result.candidate,client_order_id); executed=True; order_id=order.order_id
        await self.journal.record(id=run_id,run_id=run_id,decision_id=decision.id,symbol=request.engine_input.symbol,approved=decision.approved,executed=executed,order_id=order_id,regime=result.regime.regime,thesis=result.ai_thesis.thesis if result.ai_thesis else result.regime.rationale,quant_score=result.quant.total,rejection_reasons=list(decision.reasons),analysis={**result.analysis,"decision":{"id":decision.id,"approved":decision.approved,"reasons":list(decision.reasons)},"execution":{"executed":executed,"order_id":order_id}})
        return TradingPipelineResult(run_id,decision.id,{**result.analysis,"decision":{"id":decision.id,"approved":decision.approved,"reasons":list(decision.reasons)},"execution":{"executed":executed,"order_id":order_id}},executed,order_id)
