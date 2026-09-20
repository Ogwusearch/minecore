"""FastAPI dependency that yields a per-request session.

The session is committed when the request handler returns normally,
rolled back if it raises, and always closed. Services inside a request
therefore only need ``flush()`` to obtain IDs; the commit happens here
once, at the request boundary.
"""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
