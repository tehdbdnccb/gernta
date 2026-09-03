from __future__ import annotations
from application.trading.contracts import TradingPipelineRequest
from application.trading.pipeline import TradingPipeline

class TradingOrchestrator:
    def __init__(self,pipeline: TradingPipeline): self.pipeline=pipeline
    async def run(self,run_id:str,request:TradingPipelineRequest,client_order_id:str): return await self.pipeline.run(run_id,request,client_order_id)
