"""Mining operation service.

Enforces:

- Every operation belongs to exactly one organization.
- Every referenced entity (site, pit, material, unit, operator) must
  belong to that same organization (or be a global user).
- The pit must belong to the given mine site.
- Status transitions follow workflow.py.
- Only `draft` operations may be edited or deleted.
- Every create, update, delete and status change writes an audit entry.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit.service import log_action
from app.core.crud_service import ConflictError, ReferenceError
from app.materials.models import Material
from app.mining.models import MiningOperation
from app.mining.numbering import next_operation_number
from app.mining.workflow import (
    require_deletable,
    require_editable,
    require_transition,
)
from app.models.mine_site import MineSite
from app.models.user import User
from app.pits.models import Pit
from app.shifts.models import Shift
from app.units.models import Unit


ENTITY_TYPE = "mining_operation"


def _now() -> datetime:
    return datetime.now(timezone.utc)


class MiningOperationService:
    entity_name = "MiningOperation"

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------
    def list_for_org(
        self,
        db: Session,
        org_id: UUID,
        *,
        status: str | None = None,
        mine_site_id: UUID | None = None,
        pit_id: UUID | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[MiningOperation]:
        stmt = select(MiningOperation).where(
            MiningOperation.organization_id == org_id
        )
        if status is not None:
            stmt = stmt.where(MiningOperation.status == status)
        if mine_site_id is not None:
            stmt = stmt.where(MiningOperation.mine_site_id == mine_site_id)
        if pit_id is not None:
            stmt = stmt.where(MiningOperation.pit_id == pit_id)
        if from_date is not None:
            stmt = stmt.where(MiningOperation.operation_date >= from_date)
        if to_date is not None:
            stmt = stmt.where(MiningOperation.operation_date <= to_date)

        stmt = stmt.order_by(
            MiningOperation.operation_date.desc(),
            MiningOperation.operation_seq.desc(),
        )
        return list(db.execute(stmt).scalars().all())

    def get(
        self, db: Session, org_id: UUID, op_id: UUID
    ) -> MiningOperation | None:
        stmt = select(MiningOperation).where(
            MiningOperation.id == op_id,
            MiningOperation.organization_id == org_id,
        )
        return db.execute(stmt).scalar_one_or_none()

    # ---------------------------------------------------------
    # Reference validation
    # ---------------------------------------------------------
    def _validate_refs(self, db: Session, org_id: UUID, data: dict) -> None:
        # mine_site (required)
        site_id = data.get("mine_site_id")
        if site_id is not None:
            site = db.execute(
                select(MineSite.id).where(
                    MineSite.id == site_id,
                    MineSite.organization_id == org_id,
                )
            ).scalar_one_or_none()
            if site is None:
                raise ReferenceError(
                    f"MineSite {site_id} not found in this organization"
                )

        # pit (required) + must belong to the given site
        pit_id = data.get("pit_id")
        if pit_id is not None:
            pit = db.execute(
                select(Pit).where(
                    Pit.id == pit_id,
                    Pit.organization_id == org_id,
                )
            ).scalar_one_or_none()
            if pit is None:
                raise ReferenceError(
                    f"Pit {pit_id} not found in this organization"
                )
            expected_site = data.get("mine_site_id")
            if expected_site is not None and pit.mine_site_id != expected_site:
                raise ReferenceError(
                    f"Pit {pit_id} does not belong to MineSite {expected_site}"
                )

        # material (required)
        material_id = data.get("material_id")
        if material_id is not None:
            mat = db.execute(
                select(Material.id).where(
                    Material.id == material_id,
                    Material.organization_id == org_id,
                )
            ).scalar_one_or_none()
            if mat is None:
                raise ReferenceError(
                    f"Material {material_id} not found in this organization"
                )

        # unit (optional)
        unit_id = data.get("unit_id")
        if unit_id is not None:
            unit = db.execute(
                select(Unit.id).where(
                    Unit.id == unit_id,
                    Unit.organization_id == org_id,
                )
            ).scalar_one_or_none()
            if unit is None:
                raise ReferenceError(
                    f"Unit {unit_id} not found in this organization"
                )

        # shift (optional)
        shift_id = data.get("shift_id")
        if shift_id is not None:
            shift = db.execute(
                select(Shift.id).where(
                    Shift.id == shift_id,
                    Shift.organization_id == org_id,
                )
            ).scalar_one_or_none()
            if shift is None:
                raise ReferenceError(
                    f"Shift {shift_id} not found in this organization"
                )

        # operator (optional; user is global)
        operator_id = data.get("operator_user_id")
        if operator_id is not None:
            user = db.execute(
                select(User.id).where(User.id == operator_id)
            ).scalar_one_or_none()
            if user is None:
                raise ReferenceError(f"Operator user {operator_id} not found")

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------
    def create(
        self,
        db: Session,
        org_id: UUID,
        actor_user_id: UUID,
        payload,
    ) -> MiningOperation:
        data = payload.model_dump(exclude_unset=True)
        self._validate_refs(db, org_id, data)

        seq, number = next_operation_number(db, org_id)

        op = MiningOperation(
            organization_id=org_id,
            operation_seq=seq,
            operation_number=number,
            status="draft",
            created_by_user_id=actor_user_id,
            **data,
        )
        db.add(op)
        try:
            db.flush()
        except Exception as exc:
            db.rollback()
            raise ConflictError(str(exc)) from exc

        log_action(
            db,
            organization_id=org_id,
            actor_user_id=actor_user_id,
            entity_type=ENTITY_TYPE,
            entity_id=op.id,
            action="create",
            to_status="draft",
        )

        db.commit()
        db.refresh(op)
        return op

    # ---------------------------------------------------------
    # Update (draft only)
    # ---------------------------------------------------------
    def update(
        self,
        db: Session,
        org_id: UUID,
        actor_user_id: UUID,
        op_id: UUID,
        payload,
    ) -> MiningOperation | None:
        op = self.get(db, org_id, op_id)
        if op is None:
            return None

        require_editable(op.status)

        data = payload.model_dump(exclude_unset=True)

        # Merge into a dict that mirrors the current row so ref validation
        # can see both changed and unchanged dependencies.
        merged = {
            "mine_site_id": op.mine_site_id,
            "pit_id": data.get("pit_id", op.pit_id),
            "shift_id": data.get("shift_id", op.shift_id),
            "material_id": op.material_id,
            "unit_id": data.get("unit_id", op.unit_id),
            "operator_user_id": data.get("operator_user_id", op.operator_user_id),
        }
        self._validate_refs(db, org_id, merged)

        changes: dict = {}
        for key, new_value in data.items():
            old_value = getattr(op, key)
            if old_value == new_value:
                continue
            changes[key] = {
                "from": None if old_value is None else str(old_value),
                "to": None if new_value is None else str(new_value),
            }
            setattr(op, key, new_value)

        if changes:
            log_action(
                db,
                organization_id=org_id,
                actor_user_id=actor_user_id,
                entity_type=ENTITY_TYPE,
                entity_id=op.id,
                action="update",
                changes=changes,
            )
            try:
                db.flush()
            except Exception as exc:
                db.rollback()
                raise ConflictError(str(exc)) from exc
            db.commit()
            db.refresh(op)

        return op

    # ---------------------------------------------------------
    # Delete (draft only)
    # ---------------------------------------------------------
    def delete(
        self,
        db: Session,
        org_id: UUID,
        actor_user_id: UUID,
        op_id: UUID,
    ) -> bool:
        op = self.get(db, org_id, op_id)
        if op is None:
            return False

        require_deletable(op.status)

        log_action(
            db,
            organization_id=org_id,
            actor_user_id=actor_user_id,
            entity_type=ENTITY_TYPE,
            entity_id=op.id,
            action="delete",
            from_status=op.status,
        )

        db.delete(op)
        db.commit()
        return True

    # ---------------------------------------------------------
    # Workflow
    # ---------------------------------------------------------
    def record(
        self,
        db: Session,
        org_id: UUID,
        actor_user_id: UUID,
        op_id: UUID,
    ) -> MiningOperation | None:
        op = self.get(db, org_id, op_id)
        if op is None:
            return None

        require_transition(op.status, "recorded")
        old = op.status
        op.status = "recorded"
        op.recorded_at = _now()
        op.recorded_by_user_id = actor_user_id

        log_action(
            db,
            organization_id=org_id,
            actor_user_id=actor_user_id,
            entity_type=ENTITY_TYPE,
            entity_id=op.id,
            action="record",
            from_status=old,
            to_status="recorded",
        )
        db.flush()
        db.commit()
        db.refresh(op)
        return op

    def approve(
        self,
        db: Session,
        org_id: UUID,
        actor_user_id: UUID,
        op_id: UUID,
    ) -> MiningOperation | None:
        op = self.get(db, org_id, op_id)
        if op is None:
            return None

        require_transition(op.status, "approved")
        old = op.status
        op.status = "approved"
        op.approved_at = _now()
        op.approved_by_user_id = actor_user_id

        log_action(
            db,
            organization_id=org_id,
            actor_user_id=actor_user_id,
            entity_type=ENTITY_TYPE,
            entity_id=op.id,
            action="approve",
            from_status=old,
            to_status="approved",
        )
        db.flush()
        db.commit()
        db.refresh(op)
        return op

    def cancel(
        self,
        db: Session,
        org_id: UUID,
        actor_user_id: UUID,
        op_id: UUID,
        reason: str,
    ) -> MiningOperation | None:
        op = self.get(db, org_id, op_id)
        if op is None:
            return None

        require_transition(op.status, "cancelled")
        old = op.status
        op.status = "cancelled"
        op.cancelled_at = _now()
        op.cancelled_by_user_id = actor_user_id
        op.cancellation_reason = reason

        log_action(
            db,
            organization_id=org_id,
            actor_user_id=actor_user_id,
            entity_type=ENTITY_TYPE,
            entity_id=op.id,
            action="cancel",
            from_status=old,
            to_status="cancelled",
            changes={"reason": reason},
        )
        db.flush()
        db.commit()
        db.refresh(op)
        return op


service = MiningOperationService()
