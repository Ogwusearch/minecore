from __future__ import annotations

from pydantic import BaseModel

from app.core.schemas import ReadModel


class MineralCreate(BaseModel):
    code: str
    name: str
    description: str | None = None
    status: str = "active"


class MineralUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None


class MineralRead(ReadModel):
    code: str
    name: str
    description: str | None
    status: str
