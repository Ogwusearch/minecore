"""Transaction context manager for multi-table operations.

Commits on success, rolls back on any exception, always closes the
session. Prefer this over manually calling commit() in services.
"""
from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.db.database import SessionLocal


@contextmanager
def transaction() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
