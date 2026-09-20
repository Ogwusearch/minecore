from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import MineSite, UserSiteAssignment
from app.mine_sites.repository import MineSiteRepository, SiteAssignmentRepository
from app.mine_sites.schemas import (
    MineSiteCreate,
    MineSiteUpdate,
    SiteAssignmentCreate,
)


class MineSiteService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = MineSiteRepository(db)
        self.assignments = SiteAssignmentRepository(db)

    def list(self, organization_id: UUID) -> list[MineSite]:
        return self.repo.list_in_org(organization_id)

    def get(self, organization_id: UUID, site_id: UUID) -> MineSite:
        site = self.repo.get_in_org(organization_id, site_id)
        if site is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Mine site not found")
        return site

    def create(self, organization_id: UUID, data: MineSiteCreate) -> MineSite:
        if self.repo.find_by_code(organization_id, data.code) is not None:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Mine site code '{data.code}' already exists in this organization",
            )

        site = MineSite(
            organization_id=organization_id,
            code=data.code,
            name=data.name,
            status=data.status,
            location=data.location,
            latitude=data.latitude,
            longitude=data.longitude,
        )
        self.db.add(site)
        self.db.flush()
        self.db.refresh(site)
        return site

    def update(
        self, organization_id: UUID, site_id: UUID, data: MineSiteUpdate
    ) -> MineSite:
        site = self.get(organization_id, site_id)

        for field in ("name", "status", "location", "latitude", "longitude"):
            value = getattr(data, field)
            if value is not None:
                setattr(site, field, value)

        self.db.flush()
        self.db.refresh(site)
        return site

    def delete(self, organization_id: UUID, site_id: UUID) -> None:
        site = self.get(organization_id, site_id)
        self.db.delete(site)

    # ------------------------------------------------------------------
    # Site assignments
    # ------------------------------------------------------------------
    def list_assignments(
        self, organization_id: UUID, site_id: UUID
    ) -> list[UserSiteAssignment]:
        self.get(organization_id, site_id)
        return self.assignments.list_for_site(organization_id, site_id)

    def assign_user(
        self,
        organization_id: UUID,
        site_id: UUID,
        data: SiteAssignmentCreate,
    ) -> UserSiteAssignment:
        self.get(organization_id, site_id)

        existing = self.assignments.find(organization_id, site_id, data.user_id)
        if existing is not None:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "User is already assigned to this mine site",
            )

        assignment = UserSiteAssignment(
            organization_id=organization_id,
            mine_site_id=site_id,
            user_id=data.user_id,
        )
        self.db.add(assignment)
        self.db.flush()
        self.db.refresh(assignment)
        return assignment

    def unassign_user(
        self, organization_id: UUID, site_id: UUID, user_id: UUID
    ) -> None:
        self.get(organization_id, site_id)
        assignment = self.assignments.find(organization_id, site_id, user_id)
        if assignment is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Assignment not found")
        self.db.delete(assignment)
