from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

@dataclass(frozen=True, slots=True)
class JournalRecord:
    id: str
    run_id: str
    decision_id: str
    symbol: str
    created_at: datetime
    approved: bool
    executed: bool
    order_id: str | None
    regime: str
    thesis: str
    quant_score: float
    rejection_reasons: list[str]
    analysis: dict

class JournalRepository(Protocol):
    async def create(self, record: JournalRecord) -> JournalRecord: ...
    async def list_recent(self, limit: int) -> list[JournalRecord]: ...
    async def get_by_run_id(self, run_id: str) -> JournalRecord | None: ...

class JournalService:
    def __init__(self, repository: JournalRepository): self.repository = repository
    async def record(self, **kwargs):
        return await self.repository.create(JournalRecord(created_at=datetime.now(timezone.utc), **kwargs))
    async def list_recent(self, limit=50): return await self.repository.list_recent(min(max(limit,1),500))
    async def get_by_run_id(self, run_id): return await self.repository.get_by_run_id(run_id)
