from __future__ import annotations
import json
from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    environment: str = "paper"
    alpaca_api_key: str = ""
    alpaca_api_secret: str = ""
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/alpha_commander"
    cors_origins: list[str] = Field(default_factory=lambda: [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://alpaca-commander1-one.vercel.app"
    ])
    ai_enabled: bool = False
    ai_provider: str = ""
    ai_api_key: str = ""
    ai_model: str = ""
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            try: return json.loads(value)
            except json.JSONDecodeError: return [x.strip() for x in value.split(",") if x.strip()]
        return value

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

