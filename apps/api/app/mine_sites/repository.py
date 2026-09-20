from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MineSite, UserSiteAssignment


class MineSiteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_in_org(self, organization_id: UUID) -> list[MineSite]:
        stmt = (
            select(MineSite)
            .where(MineSite.organization_id == organization_id)
            .order_by(MineSite.code)
        )
        return list(self.db.scalars(stmt))

    def get_in_org(self, organization_id: UUID, site_id: UUID) -> MineSite | None:
        stmt = select(MineSite).where(
            MineSite.organization_id == organization_id,
            MineSite.id == site_id,
        )
        return self.db.scalars(stmt).first()

    def find_by_code(self, organization_id: UUID, code: str) -> MineSite | None:
        stmt = select(MineSite).where(
            MineSite.organization_id == organization_id,
            MineSite.code == code,
        )
        return self.db.scalars(stmt).first()


class SiteAssignmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_for_site(
        self, organization_id: UUID, site_id: UUID
    ) -> list[UserSiteAssignment]:
        stmt = (
            select(UserSiteAssignment)
            .where(
                UserSiteAssignment.organization_id == organization_id,
                UserSiteAssignment.mine_site_id == site_id,
            )
            .order_by(UserSiteAssignment.user_id)
        )
        return list(self.db.scalars(stmt))

    def find(
        self, organization_id: UUID, site_id: UUID, user_id: UUID
    ) -> UserSiteAssignment | None:
        stmt = select(UserSiteAssignment).where(
            UserSiteAssignment.organization_id == organization_id,
            UserSiteAssignment.mine_site_id == site_id,
            UserSiteAssignment.user_id == user_id,
        )
        return self.db.scalars(stmt).first()
