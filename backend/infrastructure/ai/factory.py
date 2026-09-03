from infrastructure.ai.provider_impl import build_ai_provider

def create_ai_service(settings):
    from application.ai.service import AIResearchService
    return AIResearchService(build_ai_provider(settings))
