from __future__ import annotations
from dataclasses import dataclass
from domain.broker import BrokerPort, BrokerPosition

@dataclass(frozen=True, slots=True)
class PortfolioContext:
    portfolio_value: float
    buying_power: float
    daily_pnl: float
    open_risk: float
    underlying_exposure: float
    positions: tuple[BrokerPosition, ...]

class PortfolioContextService:
    def __init__(self, broker: BrokerPort): self.broker = broker
    async def get_context(self) -> PortfolioContext:
        account = await self.broker.get_account()
        positions = tuple(await self.broker.get_positions())
        open_risk = sum(max(-p.unrealized_pnl, 0.0) for p in positions)
        exposure = sum(abs(p.market_value) for p in positions)
        return PortfolioContext(account.portfolio_value, account.buying_power, account.daily_pnl, open_risk, exposure, positions)
