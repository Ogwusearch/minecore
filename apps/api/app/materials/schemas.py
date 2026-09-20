from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.core.schemas import ReadModel


class MaterialCreate(BaseModel):
    code: str
    name: str
    description: str | None = None
    status: str = "active"
    material_type_id: UUID | None = None
    mineral_id: UUID | None = None
    unit_id: UUID | None = None


class MaterialUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    material_type_id: UUID | None = None
    mineral_id: UUID | None = None
    unit_id: UUID | None = None


class MaterialRead(ReadModel):
    code: str
    name: str
    description: str | None
    status: str
    material_type_id: UUID | None
    mineral_id: UUID | None
    unit_id: UUID | None
