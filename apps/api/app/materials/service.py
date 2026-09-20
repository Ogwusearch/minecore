from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.crud_service import CrudService, ReferenceError
from app.materials.models import Material
from app.material_types.models import MaterialType
from app.minerals.models import Mineral
from app.units.models import Unit


class MaterialService(CrudService[Material]):
    model = Material
    entity_name = "Material"

    def validate_references(self, db: Session, org_id: UUID, data: dict) -> None:
        self._check(db, org_id, data, "material_type_id", MaterialType, "MaterialType")
        self._check(db, org_id, data, "mineral_id", Mineral, "Mineral")
        self._check(db, org_id, data, "unit_id", Unit, "Unit")

    @staticmethod
    def _check(db: Session, org_id: UUID, data: dict, key: str, model, label: str) -> None:
        ref_id = data.get(key)
        if ref_id is None:
            return
        stmt = select(model.id).where(
            model.id == ref_id,
            model.organization_id == org_id,
        )
        if db.execute(stmt).scalar_one_or_none() is None:
            raise ReferenceError(f"{label} {ref_id} does not belong to this organization")


service = MaterialService()
