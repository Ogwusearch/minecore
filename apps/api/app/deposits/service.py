from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.crud_service import CrudService, ReferenceError
from app.deposits.models import Deposit
from app.minerals.models import Mineral
from app.models.mine_site import MineSite


class DepositService(CrudService[Deposit]):
    model = Deposit
    entity_name = "Deposit"

    def validate_references(self, db: Session, org_id: UUID, data: dict) -> None:
        self._check(db, org_id, data, "mine_site_id", MineSite, "MineSite", required=True)
        self._check(db, org_id, data, "primary_mineral_id", Mineral, "Mineral", required=False)

    @staticmethod
    def _check(
        db: Session,
        org_id: UUID,
        data: dict,
        key: str,
        model,
        label: str,
        *,
        required: bool,
    ) -> None:
        ref_id = data.get(key)
        if ref_id is None:
            if required:
                raise ReferenceError(f"{label} is required")
            return
        stmt = select(model.id).where(
            model.id == ref_id,
            model.organization_id == org_id,
        )
        if db.execute(stmt).scalar_one_or_none() is None:
            raise ReferenceError(f"{label} {ref_id} does not belong to this organization")


service = DepositService()
