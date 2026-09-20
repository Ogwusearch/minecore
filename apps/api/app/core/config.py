"""Application configuration.

Settings are loaded from environment variables, then from the repo-root
.env file. Environment always wins over .env, and .env always wins over
the defaults defined here.
"""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# repo root: apps/api/app/core/config.py -> parents[4] -> <repo>
_ENV_FILE = Path(__file__).resolve().parents[4] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "MineCore"
    app_env: str = "development"
    app_debug: bool = True

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_db: str = "minecore"
    postgres_user: str = "minecore"
    postgres_password: str = "minecore"

    database_url: str = "postgresql+psycopg://minecore:minecore@localhost:5433/minecore"

    jwt_secret: str = "change_this_secret"
    jwt_algorithm: str = "HS256"

    vite_api_url: str = "http://localhost:8000"


settings = Settings()
