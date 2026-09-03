from __future__ import annotations
from application.ai.provider import AIProvider
from application.ai.thesis import AIThesis

class AIResearchService:
    def __init__(self, provider: AIProvider | None = None): self.provider = provider
    async def research(self, context: dict) -> AIThesis | None:
        if self.provider is None: return None
        return await self.provider.research(context)
