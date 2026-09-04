from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    environment: str = "paper"
    alpaca_api_key: str = ""
    alpaca_api_secret: str = ""
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/alpha_commander"
    cors_origins_raw: str = "https://alpaca-commander1-one.vercel.app,http://localhost:5173,http://127.0.0.1:5173"
    ai_enabled: bool = False
    ai_provider: str = ""
    ai_api_key: str = ""
    ai_model: str = ""
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]

    def validate_runtime(self) -> None:
        if self.environment not in {"paper", "live", "test"}:
            raise ValueError("ENVIRONMENT must be paper, live, or test")
        if self.environment != "test" and (not self.alpaca_api_key or not self.alpaca_api_secret):
            raise ValueError("ALPACA_API_KEY and ALPACA_API_SECRET are required")
        if self.environment == "live":
            raise ValueError("Live trading is intentionally disabled in this build")
        if self.ai_enabled and not self.ai_api_key:
            raise ValueError("AI_API_KEY is required when AI_ENABLED=true")

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_runtime()
    return settings
