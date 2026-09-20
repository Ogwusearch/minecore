"""Shared pytest fixtures for MineCore tests.

Two families of fixtures:

* ``db``       — raw psycopg connection for DDL / constraint tests.
* ``db_session`` / ``api_client`` — SQLAlchemy-backed for integration tests.

Every fixture wraps the test in an outer transaction that is always
rolled back. The ``api_client`` override of ``get_db`` uses the same
connection and commits its savepoint on success, so writes made by an
API request become visible to subsequent requests in the same test but
never leak past the outer rollback.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def _sa_url(url: str) -> str:
    """Force SQLAlchemy to use psycopg3, matching app.db.database._sa_url."""
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url



ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"


def _load_env_file(path: Path) -> None:
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


_load_env_file(ENV_FILE)


DEFAULT_DATABASE_URL = "postgresql+psycopg://minecore:minecore@localhost:5433/minecore"
DATABASE_URL = os.environ.get("DATABASE_URL_SYNC", DEFAULT_DATABASE_URL.replace("+psycopg", ""))


@pytest.fixture(scope="session")
def database_url() -> str:
    return DATABASE_URL


# ---------------------------------------------------------------------------
# psycopg fixture — the "db" fixture from Phase 01
# ---------------------------------------------------------------------------
@pytest.fixture
def db(database_url: str):
    import psycopg

    raw_url = database_url.replace("postgresql+psycopg://", "postgresql://")
    with psycopg.connect(raw_url) as conn:
        with conn.transaction(force_rollback=True):
            yield conn


# ---------------------------------------------------------------------------
# SQLAlchemy fixtures — Phase 03+
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def engine(database_url: str):
    eng = create_engine(_sa_url(database_url), future=True)
    yield eng
    eng.dispose()


@pytest.fixture
def db_connection(engine):
    """Outer connection wrapped in a rollback-only transaction."""
    conn = engine.connect()
    trans = conn.begin()
    try:
        yield conn
    finally:
        trans.rollback()
        conn.close()


@pytest.fixture
def db_session(db_connection) -> Session:
    """SQLAlchemy session bound to the test's outer transaction.

    Writes made here are flushed to the DB but live inside a savepoint
    on the shared connection, so the API client (also bound to
    ``db_connection``) can read them.
    """
    session = Session(bind=db_connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def api_client(db_connection):
    """FastAPI TestClient sharing the test's connection.

    The override of ``get_db`` mirrors ``app.db.session.get_db`` exactly:
    commit on success, rollback on error, close in finally. In savepoint
    mode the commit only releases the savepoint, so the outer
    transaction still rolls back at teardown.
    """
    from fastapi.testclient import TestClient

    from app.db.session import get_db
    from app.main import app

    def override_get_db():
        session = Session(bind=db_connection, join_transaction_mode="create_savepoint")
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
