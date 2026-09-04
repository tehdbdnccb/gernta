from __future__ import annotations
import json
from functools import lru_cache
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    environment: str = "paper"
    alpaca_api_key: str = ""
    alpaca_api_secret: str = ""
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/alpha_commander"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"])
    ai_enabled: bool = False
    ai_provider: str = ""
    ai_api_key: str = ""
    ai_model: str = ""
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False, json_schema_extra={"cors_origins": {"json_schema_input_type": "string"}})

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return ["http://localhost:5173", "http://127.0.0.1:5173"]
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
            return [x.strip() for x in value.split(",") if x.strip()]
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

