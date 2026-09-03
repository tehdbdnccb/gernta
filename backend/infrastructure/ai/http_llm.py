from __future__ import annotations
import json
import httpx
from application.ai.thesis import AIThesis

class HttpLLMProvider:
    def __init__(self, api_key: str, model: str, endpoint: str = "https://api.openai.com/v1/chat/completions"):
        self.api_key, self.model, self.endpoint = api_key, model, endpoint

    async def research(self, context: dict) -> AIThesis:
        prompt = "Return strict JSON with thesis, confidence, catalysts, risks, recommendation. Context: " + json.dumps(context)
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(self.endpoint, headers={"Authorization": f"Bearer {self.api_key}"}, json={"model": self.model, "messages":[{"role":"user","content":prompt}], "temperature":0.1})
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        return AIThesis(str(data["thesis"]), float(data["confidence"]), tuple(data.get("catalysts", [])), tuple(data.get("risks", [])), str(data["recommendation"]))
