from infrastructure.ai.http_llm import HttpLLMProvider

def build_ai_provider(settings):
    if not settings.ai_enabled: return None
    if settings.ai_provider.lower() in {"openai", "openai-compatible", ""}:
        return HttpLLMProvider(settings.ai_api_key, settings.ai_model)
    raise ValueError(f"Unsupported AI_PROVIDER: {settings.ai_provider}")
