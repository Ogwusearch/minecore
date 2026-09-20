"""Per-organization operation numbering.

Format: MO-{YYYY}-{seq:06d}   e.g. MO-2026-000042

Concurrency: the owning organization row is locked FOR UPDATE for the
duration of the current transaction. Two concurrent creates in the same
org serialize on that lock, so both see a monotonically increasing
sequence. Concurrent creates in different orgs do not block each other.
"""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.organization import Organization


def next_operation_number(db: Session, organization_id: UUID) -> tuple[int, str]:
    # Serialize numbering per organization.
    db.execute(
        select(Organization.id)
        .where(Organization.id == organization_id)
        .with_for_update()
    )

    from app.mining.models import MiningOperation  # local import avoids cycle

    max_seq = db.execute(
        select(func.coalesce(func.max(MiningOperation.operation_seq), 0)).where(
            MiningOperation.organization_id == organization_id
        )
    ).scalar_one()

    seq = int(max_seq) + 1
    year = datetime.now(timezone.utc).year
    number = f"MO-{year}-{seq:06d}"
    return seq, number
