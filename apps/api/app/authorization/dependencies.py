from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends
from psycopg import Connection

from app.auth.dependencies import AuthenticatedUser, get_current_user
from .permissions import Permission
from .service import require_permission


def require_permission_dependency(
    permission: Permission,
) -> Callable:
    def dependency(
        db: Connection,
        user: AuthenticatedUser = Depends(get_current_user),
    ) -> None:
        if not user.organization_id:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Organization context required",
            )

        require_permission(
            db,
            user_id=user.id,
            organization_id=user.organization_id,
            permission=permission,
        )

    return dependency