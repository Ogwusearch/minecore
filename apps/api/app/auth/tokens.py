from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt


JWT_SECRET = os.environ.get("JWT_SECRET")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET must be configured")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30


def create_access_token(
    *,
    user_id: str,
    organization_id: str | None = None,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": user_id,
        "organization_id": organization_id,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )