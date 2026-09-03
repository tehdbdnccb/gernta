from __future__ import annotations
from uuid import uuid4
from application.trading.request_factory import build_request

class TradingRunManager:
    def __init__(self,pipeline): self.pipeline=pipeline
    async def run(self,symbol,portfolio_context,realized_daily_pnl=0.0,unrealized_daily_pnl=0.0,client_order_id=None):
        run_id=str(uuid4()); client_order_id=client_order_id or f"alpha-{run_id}"
        request=build_request(symbol,realized_daily_pnl,unrealized_daily_pnl,portfolio_context)
        return await self.pipeline.run(run_id,request,client_order_id)
