from __future__ import annotations

from pydantic import BaseModel

from app.core.schemas import ReadModel


class MaterialTypeCreate(BaseModel):
    code: str
    name: str
    description: str | None = None
    status: str = "active"


class MaterialTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None


class MaterialTypeRead(ReadModel):
    code: str
    name: str
    description: str | None
    status: str
