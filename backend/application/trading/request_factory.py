from application.trading.contracts import TradingEngineInput, TradingPipelineRequest

def build_request(symbol:str, realized_daily_pnl:float, unrealized_daily_pnl:float, portfolio_context):
    return TradingPipelineRequest(TradingEngineInput(symbol.strip().upper(),realized_daily_pnl,unrealized_daily_pnl),portfolio_context)
