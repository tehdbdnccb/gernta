from __future__ import annotations
from typing import Protocol
from application.ai.thesis import AIThesis

class AIProvider(Protocol):
    async def research(self, context: dict) -> AIThesis: ...
