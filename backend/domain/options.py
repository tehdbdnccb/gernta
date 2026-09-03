from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Literal

OptionType = Literal["call", "put"]

@dataclass(frozen=True, slots=True)
class OptionContract:
    symbol: str
    underlying_symbol: str
    expiration_date: date
    strike_price: float
    option_type: OptionType
    bid: float
    ask: float
    mark: float
    implied_volatility: float | None = None
    delta: float | None = None

    @property
    def spread(self) -> float:
        return max(self.ask - self.bid, 0.0)

@dataclass(frozen=True, slots=True)
class OptionCandidate:
    strategy: str
    underlying_symbol: str
    long_leg: OptionContract
    short_leg: OptionContract
    debit: float
    max_loss: float
    max_profit: float
    width: float
    expiration_date: date
