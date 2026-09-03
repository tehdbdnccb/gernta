from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AIThesis:
    thesis: str
    confidence: float
    catalysts: tuple[str, ...]
    risks: tuple[str, ...]
    recommendation: str
