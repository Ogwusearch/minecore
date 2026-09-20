"""Audit trail helpers.

Entries are append-only by design. There is no update or delete helper
here on purpose — the audit trail must not be modifiable through the
application layer.
"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit.models import AuditLog


def log_action(
    db: Session,
    *,
    organization_id: UUID,
    actor_user_id: UUID | None,
    entity_type: str,
    entity_id: UUID,
    action: str,
    from_status: str | None = None,
    to_status: str | None = None,
    changes: dict | None = None,
) -> AuditLog:
    entry = AuditLog(
        organization_id=organization_id,
        actor_user_id=actor_user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        from_status=from_status,
        to_status=to_status,
        changes=changes,
    )
    db.add(entry)
    db.flush()
    return entry


def list_for_entity(
    db: Session,
    *,
    organization_id: UUID,
    entity_type: str,
    entity_id: UUID,
) -> list[AuditLog]:
    stmt = (
        select(AuditLog)
        .where(
            AuditLog.organization_id == organization_id,
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id,
        )
        .order_by(AuditLog.created_at.asc())
    )
    return list(db.execute(stmt).scalars().all())
