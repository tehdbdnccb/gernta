from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.persistence.database import Base

class JournalModel(Base):
    __tablename__="decision_journal"
    id: Mapped[str]=mapped_column(String(64),primary_key=True)
    run_id: Mapped[str]=mapped_column(String(64),unique=True,index=True)
    decision_id: Mapped[str]=mapped_column(String(64),index=True)
    symbol: Mapped[str]=mapped_column(String(16),index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),index=True)
    approved: Mapped[bool]=mapped_column(Boolean,index=True)
    executed: Mapped[bool]=mapped_column(Boolean,index=True)
    order_id: Mapped[str|None]=mapped_column(String(128),nullable=True)
    regime: Mapped[str]=mapped_column(String(32))
    thesis: Mapped[str]=mapped_column(String(4000))
    quant_score: Mapped[float]=mapped_column(Float)
    rejection_reasons: Mapped[list]=mapped_column(JSON,default=list)
    analysis: Mapped[dict]=mapped_column(JSON)
