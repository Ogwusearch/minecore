from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .tokens import decode_access_token


bearer = HTTPBearer()


@dataclass(frozen=True)
class AuthenticatedUser:
    id: str
    organization_id: str | None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> AuthenticatedUser:
    try:
        payload = decode_access_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        ) from exc

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    return AuthenticatedUser(
        id=user_id,
        organization_id=payload.get("organization_id"),
    )