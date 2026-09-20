from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Organization


class OrganizationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_in_scope(self, organization_id: UUID) -> Organization | None:
        stmt = select(Organization).where(Organization.id == organization_id)
        return self.db.scalars(stmt).first()
