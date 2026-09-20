from __future__ import annotations

from datetime import time
from uuid import UUID

from pydantic import BaseModel

from app.core.schemas import ReadModel


class ShiftCreate(BaseModel):
    code: str
    name: str
    start_time: time
    end_time: time
    status: str = "active"
    mine_site_id: UUID | None = None


class ShiftUpdate(BaseModel):
    name: str | None = None
    start_time: time | None = None
    end_time: time | None = None
    status: str | None = None
    mine_site_id: UUID | None = None


class ShiftRead(ReadModel):
    code: str
    name: str
    start_time: time
    end_time: time
    status: str
    mine_site_id: UUID | None
