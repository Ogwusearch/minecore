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
