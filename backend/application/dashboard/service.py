from __future__ import annotations
from dataclasses import asdict
from application.portfolio.context import PortfolioContextService
from application.trading.journal import JournalService

class DashboardService:
    def __init__(self,portfolio_service:PortfolioContextService,journal_service:JournalService): self.portfolio_service,self.journal_service=portfolio_service,journal_service
    async def portfolio(self):
        c=await self.portfolio_service.get_context()
        return {"account":{"portfolio_value":c.portfolio_value,"buying_power":c.buying_power,"daily_pnl":c.daily_pnl,"open_risk":c.open_risk,"underlying_exposure":c.underlying_exposure,"position_count":len(c.positions)},"positions":[asdict(p) for p in c.positions]}
    async def journal(self,limit=50):
        return [asdict(x) for x in await self.journal_service.list_recent(limit)]
    async def trade_analysis(self,run_id):
        e=await self.journal_service.get_by_run_id(run_id)
        if e is None: raise LookupError(f"Trading run '{run_id}' was not found.")
        return e.analysis
