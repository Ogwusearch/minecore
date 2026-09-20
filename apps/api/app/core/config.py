"""Application configuration.

Loads environment variables in this order:

1. The process environment (highest priority — CI, docker, shell exports)
2. The repo-root .env file
3. Defaults defined on the Settings class

The .env file is read twice on purpose:

- Once manually into os.environ, so module-level code (e.g.
  app.auth.tokens) that reads os.environ["JWT_SECRET"] directly can see
  it. pydantic-settings does NOT write to os.environ.
- Once by pydantic-settings, so the typed Settings object is populated.

This makes `uvicorn app.main:app` behave the same as `make migrate`,
`make seed`, and pytest, all of which rely on .env being visible.
"""
from __future__ import annotations

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# apps/api/app/core/config.py -> parents[4] -> repo root
_ENV_FILE = Path(__file__).resolve().parents[4] / ".env"


def _load_env_into_environ(path: Path) -> None:
    """Read simple KEY=VALUE lines from .env into os.environ.

    Existing environment variables are never overwritten, so anything the
    shell or CI has already exported takes precedence.
    """
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key:
            os.environ.setdefault(key, value)


_load_env_into_environ(_ENV_FILE)


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

    database_url: str = "postgresql://minecore:minecore@localhost:5433/minecore"

    jwt_secret: str = "change_this_secret"
    jwt_algorithm: str = "HS256"

    vite_api_url: str = "http://localhost:8000"


settings = Settings()
