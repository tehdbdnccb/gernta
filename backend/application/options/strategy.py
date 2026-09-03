from __future__ import annotations
from application.market.regime import MarketRegime
from domain.options import OptionCandidate, OptionContract

class DefinedRiskStrategy:
    def build(self, regime: MarketRegime, contracts: list[OptionContract], price: float, max_debit: float = 5.0) -> OptionCandidate | None:
        if regime not in {"bullish", "bearish"}: return None
        typ = "call" if regime == "bullish" else "put"
        usable = [c for c in contracts if c.option_type == typ and c.bid >= 0 and c.ask > 0]
        if not usable: return None
        usable.sort(key=lambda c: abs(c.strike_price - price))
        long = usable[0]
        shorts = [c for c in usable[1:] if (c.strike_price > long.strike_price if typ == "call" else c.strike_price < long.strike_price)]
        if not shorts: return None
        short = min(shorts, key=lambda c: abs((c.strike_price - long.strike_price) - price * .03))
        debit = max(long.ask - short.bid, 0.0)
        width = abs(short.strike_price - long.strike_price)
        if debit <= 0 or debit > max_debit or width <= debit: return None
        return OptionCandidate("call_debit_spread" if typ == "call" else "put_debit_spread", long.underlying_symbol, long, short, debit, debit * 100, (width - debit) * 100, width, long.expiration_date)
