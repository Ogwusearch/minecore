from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Organization
from app.organizations.repository import OrganizationRepository
from app.organizations.schemas import OrganizationUpdate


class OrganizationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = OrganizationRepository(db)

    def get_current(self, organization_id: UUID) -> Organization:
        org = self.repo.get_in_scope(organization_id)
        if org is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )
        return org

    def update(self, organization_id: UUID, data: OrganizationUpdate) -> Organization:
        org = self.get_current(organization_id)

        if data.name is not None:
            org.name = data.name
        if data.status is not None:
            org.status = data.status

        self.db.flush()
        self.db.refresh(org)
        return org
