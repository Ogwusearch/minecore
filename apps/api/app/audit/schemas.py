from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_user_id: UUID | None
    entity_type: str
    entity_id: UUID
    action: str
    from_status: str | None
    to_status: str | None
    changes: dict | None
    created_at: datetime
