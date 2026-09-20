from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.core.schemas import ReadModel


class PitCreate(BaseModel):
    code: str
    name: str
    status: str = "active"
    mine_site_id: UUID
    deposit_id: UUID | None = None
    depth_m: Decimal | None = None


class PitUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    deposit_id: UUID | None = None
    depth_m: Decimal | None = None


class PitRead(ReadModel):
    code: str
    name: str
    status: str
    mine_site_id: UUID
    deposit_id: UUID | None
    depth_m: Decimal | None
