#!/usr/bin/env python3
"""
config.py - Application configuration using pydantic-settings

Autor: Homero Thompson del Lago del Terror
"""

from enum import Enum
from functools import lru_cache
from typing import Literal

from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Available environments."""

    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Environment
    environment: Environment = Environment.DEV
    debug: bool = False

    # App
    app_name: str = "FastAPI Project"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # CORS
    enable_cors: bool = True
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    database_url: PostgresDsn = "postgresql+asyncpg://user:password@localhost:5432/db"
    db_pool_size: int = 20
    db_max_overflow: int = 10
    db_echo: bool = False  # SQL logging

    # Redis
    redis_url: RedisDsn = "redis://localhost:6379/0"
    cache_ttl: int = 300  # 5 minutes default

    # Auth & Security
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Rate Limiting
    rate_limit_per_minute: int = 60

    # Features
    enable_docs: bool = True
    enable_swagger_ui: bool = True
    enable_redoc: bool = True

    # External Services (examples)
    # external_api_url: str = "https://api.example.com"
    # external_api_key: str = ""

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_dev(self) -> bool:
        """Check if running in development."""
        return self.environment == Environment.DEV

    @property
    def is_prod(self) -> bool:
        """Check if running in production."""
        return self.environment == Environment.PROD

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Singleton instance
settings = get_settings()
