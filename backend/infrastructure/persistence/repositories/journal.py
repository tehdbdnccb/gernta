from __future__ import annotations
from sqlalchemy import select
from infrastructure.persistence.models import JournalModel
from application.trading.journal import JournalRecord

class SQLJournalRepository:
    def __init__(self,session_factory): self.session_factory=session_factory
    @staticmethod
    def _record(m): return JournalRecord(m.id,m.run_id,m.decision_id,m.symbol,m.created_at,m.approved,m.executed,m.order_id,m.regime,m.thesis,m.quant_score,m.rejection_reasons or [],m.analysis)
    async def create(self,record):
        async with self.session_factory() as session:
            model=JournalModel(id=record.id,run_id=record.run_id,decision_id=record.decision_id,symbol=record.symbol,created_at=record.created_at,approved=record.approved,executed=record.executed,order_id=record.order_id,regime=record.regime,thesis=record.thesis,quant_score=record.quant_score,rejection_reasons=record.rejection_reasons,analysis=record.analysis)
            session.add(model); await session.commit(); return record
    async def list_recent(self,limit):
        async with self.session_factory() as session:
            rows=(await session.execute(select(JournalModel).order_by(JournalModel.created_at.desc()).limit(limit))).scalars().all(); return [self._record(x) for x in rows]
    async def get_by_run_id(self,run_id):
        async with self.session_factory() as session:
            row=(await session.execute(select(JournalModel).where(JournalModel.run_id==run_id))).scalar_one_or_none(); return self._record(row) if row else None
