from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.crud_service import CrudService, ReferenceError
from app.models.mine_site import MineSite
from app.shifts.models import Shift


class ShiftService(CrudService[Shift]):
    model = Shift
    entity_name = "Shift"

    def validate_references(self, db: Session, org_id: UUID, data: dict) -> None:
        site_id = data.get("mine_site_id")
        if site_id is None:
            return
        stmt = select(MineSite.id).where(
            MineSite.id == site_id,
            MineSite.organization_id == org_id,
        )
        if db.execute(stmt).scalar_one_or_none() is None:
            raise ReferenceError(f"MineSite {site_id} does not belong to this organization")


service = ShiftService()
