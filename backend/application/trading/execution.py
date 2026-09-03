from __future__ import annotations
from domain.broker import BrokerPort, OrderResult
from domain.options import OptionCandidate

class ExecutionService:
    def __init__(self, broker: BrokerPort): self.broker = broker
    async def execute(self, candidate: OptionCandidate, client_order_id: str, qty: int = 1) -> OrderResult:
        legs = [
            {"symbol": candidate.long_leg.symbol, "side": "buy", "position_intent": "buy_to_open", "ratio_qty": 1},
            {"symbol": candidate.short_leg.symbol, "side": "sell", "position_intent": "sell_to_open", "ratio_qty": 1},
        ]
        return await self.broker.submit_option_spread(legs, qty, round(candidate.debit, 2), client_order_id)
