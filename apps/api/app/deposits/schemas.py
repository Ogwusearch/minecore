from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.core.schemas import ReadModel


class DepositCreate(BaseModel):
    code: str
    name: str
    description: str | None = None
    status: str = "active"
    mine_site_id: UUID
    primary_mineral_id: UUID | None = None


class DepositUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    primary_mineral_id: UUID | None = None


class DepositRead(ReadModel):
    code: str
    name: str
    description: str | None
    status: str
    mine_site_id: UUID
    primary_mineral_id: UUID | None
