"""Application settings, loaded from environment / .env via pydantic-settings."""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central, typed configuration object.

    Values are read from environment variables or a local .env file.
    See .env.example for the full list.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Telegram
    bot_token: str = Field(..., alias="BOT_TOKEN")
    bot_username: str = Field(..., alias="BOT_USERNAME")

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./anon_bot.sqlite3", alias="DATABASE_URL"
    )

    # App
    log_level: str = Field(default="info", alias="LOG_LEVEL")

    # Rate limiting / anti-spam
    rate_limit_max_messages: int = Field(default=5, alias="RATE_LIMIT_MAX_MESSAGES")
    rate_limit_window_seconds: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")
    rate_limit_cooldown_seconds: int = Field(default=2, alias="RATE_LIMIT_COOLDOWN_SECONDS")

    # Limits
    max_message_length: int = Field(default=4000, alias="MAX_MESSAGE_LENGTH")

    def deep_link(self, token: str) -> str:
        """Build a public deep link for a given user token."""
        return f"https://t.me/{self.bot_username}?start={token}"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (read once per process)."""
    return Settings()  # type: ignore[call-arg]
