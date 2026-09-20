from __future__ import annotations

from fastapi import HTTPException, status
from psycopg import Connection

from .passwords import hash_password, verify_password


def register_user(
    db: Connection,
    *,
    email: str,
    name: str,
    password: str,
) -> str:
    existing = db.execute(
        """
        SELECT id
        FROM users
        WHERE lower(email) = lower(%s)
        """,
        (email,),
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    password_hash = hash_password(password)

    row = db.execute(
        """
        INSERT INTO users (
            email,
            name,
            password_hash,
            active
        )
        VALUES (%s, %s, %s, TRUE)
        RETURNING id
        """,
        (
            email,
            name,
            password_hash,
        ),
    ).fetchone()

    if row is None:
        raise RuntimeError("Failed to create user")

    return str(row[0])


def authenticate_user(
    db: Connection,
    *,
    email: str,
    password: str,
):
    row = db.execute(
        """
        SELECT
            id,
            email,
            name,
            password_hash,
            active
        FROM users
        WHERE lower(email) = lower(%s)
        """,
        (email,),
    ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    user_id, user_email, name, password_hash, active = row

    if not active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    if not verify_password(password, password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return {
        "id": str(user_id),
        "email": user_email,
        "name": name,
        "active": active,
    }