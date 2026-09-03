from __future__ import annotations
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Request
from application.trading.runner import TradingRunManager

router=APIRouter(tags=["trading"])
class TradeRequest(BaseModel):
    client_order_id:str|None=Field(default=None,max_length=128)
    realized_daily_pnl:float=0.0
    unrealized_daily_pnl:float=0.0

@router.post("/trade/{symbol}")
async def trade(symbol:str,body:TradeRequest,request:Request):
    manager:TradingRunManager=request.app.state.trading_manager
    portfolio=await request.app.state.portfolio_context_service.get_context()
    try:
        result=await manager.run(symbol,portfolio,body.realized_daily_pnl,body.unrealized_daily_pnl,body.client_order_id)
    except Exception as exc:
        request.app.state.logger.exception("trade_failed",extra={"symbol":symbol})
        raise HTTPException(502,"Trading pipeline failed") from exc
    return {"run_id":result.run_id,"decision_id":result.decision_id,"symbol":symbol.upper(),"approved":result.analysis["decision"]["approved"],"executed":result.executed,"order_id":result.order_id,"rejection_reasons":result.analysis["decision"]["reasons"]}
