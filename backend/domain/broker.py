from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True, slots=True)
class BrokerAccount:
    portfolio_value: float
    buying_power: float
    daily_pnl: float

@dataclass(frozen=True, slots=True)
class BrokerPosition:
    symbol: str
    quantity: float
    average_price: float
    market_value: float
    unrealized_pnl: float
    side: str

@dataclass(frozen=True, slots=True)
class OrderResult:
    order_id: str
    status: str
    client_order_id: str

class BrokerPort(Protocol):
    async def get_account(self) -> BrokerAccount: ...
    async def get_positions(self) -> list[BrokerPosition]: ...
    async def submit_option_spread(self, legs: list[dict], qty: int, limit_price: float, client_order_id: str) -> OrderResult: ...
