from __future__ import annotations
import asyncio
from domain.broker import BrokerAccount, BrokerPosition, OrderResult
from alpaca.trading.requests import LimitOrderRequest, OptionLegRequest
from alpaca.trading.enums import OrderClass, OrderSide, TimeInForce, PositionIntent

class AlpacaBroker:
    def __init__(self, clients): self.clients = clients

    async def get_account(self) -> BrokerAccount:
        a = await asyncio.to_thread(self.clients.trading.get_account)
        equity = float(a.equity)
        last_equity = float(a.last_equity or equity)
        return BrokerAccount(float(a.portfolio_value), float(a.buying_power), equity - last_equity)

    async def get_positions(self) -> list[BrokerPosition]:
        positions = await asyncio.to_thread(self.clients.trading.get_all_positions)
        return [BrokerPosition(str(p.symbol), float(p.qty), float(p.avg_entry_price), float(p.market_value), float(p.unrealized_pl), str(p.side)) for p in positions]

    async def submit_option_spread(self, legs: list[dict], qty: int, limit_price: float, client_order_id: str) -> OrderResult:
        request = LimitOrderRequest(
            qty=qty, limit_price=limit_price, side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY, order_class=OrderClass.MLEG,
            legs=[OptionLegRequest(symbol=x["symbol"], ratio_qty=x.get("ratio_qty", 1), side=OrderSide(x["side"]), position_intent=PositionIntent(x["position_intent"])) for x in legs],
            client_order_id=client_order_id,
        )
        order = await asyncio.to_thread(self.clients.trading.submit_order, request)
        return OrderResult(str(order.id), str(order.status), str(order.client_order_id))
