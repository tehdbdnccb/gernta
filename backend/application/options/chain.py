from __future__ import annotations
from datetime import date
from domain.options import OptionContract

class OptionChainService:
    def __init__(self, provider): self.provider = provider
    async def get(self, symbol: str) -> list[OptionContract]: return await self.provider.get_chain(symbol)
