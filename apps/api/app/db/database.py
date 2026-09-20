"""SQLAlchemy engine, session factory and declarative base.

DDL is owned by database/migrations/*.sql. This module only provides
the runtime ORM plumbing.

The project venv ships psycopg3, not psycopg2. SQLAlchemy's default
driver for a bare `postgresql://` URL is psycopg2, so we rewrite the
scheme to `postgresql+psycopg://` before handing it to create_engine.
The rewrite happens here and only here, so `.env` can keep a single
plain URL that every component (raw psycopg, SQLAlchemy) understands.
"""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


def _sa_url(url: str) -> str:
    """Force the psycopg3 driver for SQLAlchemy."""
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


engine = create_engine(
    _sa_url(settings.database_url),
    pool_pre_ping=True,
    future=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


class Base(DeclarativeBase):
    """Declarative base for all MineCore ORM models."""
