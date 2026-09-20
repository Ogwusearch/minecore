"""Generic CRUD service.

Every Phase 04 entity is organization-scoped and follows the same
pattern. Subclasses declare `model` and `entity_name`, and override
`validate_references` if the entity has foreign keys that must belong
to the same organization.
"""
from __future__ import annotations

from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import Base


ModelT = TypeVar("ModelT", bound=Base)


class ConflictError(Exception):
    """Raised when a create/update violates a uniqueness constraint."""


class ReferenceError(Exception):
    """Raised when a foreign key references a row outside the org."""


class CrudService(Generic[ModelT]):
    model: type[ModelT]
    entity_name: str = "Record"

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------
    def list_for_org(self, db: Session, org_id: UUID) -> list[ModelT]:
        stmt = (
            select(self.model)
            .where(self.model.organization_id == org_id)
            .order_by(self.model.created_at.desc())
        )
        return list(db.execute(stmt).scalars().all())

    def get(self, db: Session, org_id: UUID, item_id: UUID) -> ModelT | None:
        stmt = select(self.model).where(
            self.model.id == item_id,
            self.model.organization_id == org_id,
        )
        return db.execute(stmt).scalar_one_or_none()

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------
    def create(self, db: Session, org_id: UUID, payload: Any) -> ModelT:
        data = payload.model_dump(exclude_unset=True)
        self.validate_references(db, org_id, data)

        item = self.model(organization_id=org_id, **data)
        db.add(item)
        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            raise ConflictError(str(exc.orig)) from exc

        db.commit()
        db.refresh(item)
        return item

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------
    def update(self, db: Session, org_id: UUID, item_id: UUID, payload: Any) -> ModelT | None:
        item = self.get(db, org_id, item_id)
        if item is None:
            return None

        data = payload.model_dump(exclude_unset=True)
        self.validate_references(db, org_id, data)

        for key, value in data.items():
            setattr(item, key, value)

        try:
            db.flush()
        except IntegrityError as exc:
            db.rollback()
            raise ConflictError(str(exc.orig)) from exc

        db.commit()
        db.refresh(item)
        return item

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------
    def delete(self, db: Session, org_id: UUID, item_id: UUID) -> bool:
        item = self.get(db, org_id, item_id)
        if item is None:
            return False
        db.delete(item)
        db.commit()
        return True

    # ---------------------------------------------------------
    # Hook
    # ---------------------------------------------------------
    def validate_references(self, db: Session, org_id: UUID, data: dict) -> None:
        """Override to verify foreign keys belong to `org_id`."""
        return None
