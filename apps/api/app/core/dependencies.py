"""Request-scoped dependencies.

`current_organization_id` is a placeholder that will be replaced in
Phase 02 when authentication and RBAC land. For now it accepts the
organization id via an `X-Organization-Id` header so Phase 04 endpoints
can be exercised and tested.
"""
from __future__ import annotations

from uuid import UUID

from fastapi import Header, HTTPException, status


async def current_organization_id(
    x_organization_id: UUID | None = Header(default=None, alias="X-Organization-Id"),
) -> UUID:
    if x_organization_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Organization-Id header",
        )
    return x_organization_id


async def current_user_id(
    x_user_id: UUID | None = Header(default=None, alias="X-User-Id"),
) -> UUID:
    """Placeholder user dependency for Phase 05.

    The audit trail records an actor for every change. Until Phase 02's
    JWT authentication is wired through, this reads the user id from an
    `X-User-Id` header (mirrors the `X-Organization-Id` placeholder used
    by Phase 04). When the JWT dependency lands, replace the body with
    the token decoder — the signature stays the same.
    """
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication",
        )
    return x_user_id
