from __future__ import annotations

from fastapi import HTTPException, status
from psycopg import Connection

from .permissions import Permission


def require_permission(
    db: Connection,
    *,
    user_id: str,
    organization_id: str,
    permission: Permission,
) -> None:
    row = db.execute(
        """
        SELECT 1
        FROM organization_memberships om
        JOIN role_permissions rp
          ON rp.role_id = om.role_id
        JOIN permissions p
          ON p.id = rp.permission_id
        WHERE om.user_id = %s
          AND om.organization_id = %s
          AND om.active = TRUE
          AND p.name = %s
        LIMIT 1
        """,
        (
            user_id,
            organization_id,
            permission.value,
        ),
    ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )


def require_site_access(
    db: Connection,
    *,
    user_id: str,
    organization_id: str,
    site_id: str,
) -> None:
    row = db.execute(
        """
        SELECT 1
        FROM site_memberships sm
        JOIN organization_memberships om
          ON om.user_id = sm.user_id
         AND om.organization_id = sm.organization_id
        WHERE sm.user_id = %s
          AND sm.organization_id = %s
          AND sm.site_id = %s
          AND sm.active = TRUE
          AND om.active = TRUE
        LIMIT 1
        """,
        (
            user_id,
            organization_id,
            site_id,
        ),
    ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Site access denied",
        )