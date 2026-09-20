from __future__ import annotations

from pydantic import BaseModel

from app.core.schemas import ReadModel


class UnitCreate(BaseModel):
    code: str
    name: str
    symbol: str
    dimension: str
    status: str = "active"


class UnitUpdate(BaseModel):
    name: str | None = None
    symbol: str | None = None
    dimension: str | None = None
    status: str | None = None


class UnitRead(ReadModel):
    code: str
    name: str
    symbol: str
    dimension: str
    status: str
