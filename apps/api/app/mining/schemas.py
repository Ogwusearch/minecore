from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.schemas import ReadModel


class MiningOperationCreate(BaseModel):
    mine_site_id: UUID
    pit_id: UUID
    shift_id: UUID | None = None
    material_id: UUID
    unit_id: UUID | None = None
    operation_date: date
    quantity: Decimal = Field(gt=0)
    operator_user_id: UUID | None = None
    operator_name: str | None = None
    equipment_note: str | None = None
    notes: str | None = None


class MiningOperationUpdate(BaseModel):
    """Only fields editable while the operation is in `draft`.

    `mine_site_id` and `material_id` are intentionally not updatable —
    changing the site or the material after the fact would silently
    change the meaning of an operation. Create a new one instead.
    """
    pit_id: UUID | None = None
    shift_id: UUID | None = None
    unit_id: UUID | None = None
    operation_date: date | None = None
    quantity: Decimal | None = Field(default=None, gt=0)
    operator_user_id: UUID | None = None
    operator_name: str | None = None
    equipment_note: str | None = None
    notes: str | None = None


class MiningOperationRead(ReadModel):
    operation_seq: int
    operation_number: str
    mine_site_id: UUID
    pit_id: UUID
    shift_id: UUID | None
    material_id: UUID
    unit_id: UUID | None
    operation_date: date
    quantity: Decimal
    operator_user_id: UUID | None
    operator_name: str | None
    equipment_note: str | None
    notes: str | None
    status: str
    recorded_at: datetime | None
    approved_at: datetime | None
    cancelled_at: datetime | None
    cancellation_reason: str | None


class CancelRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=500)
