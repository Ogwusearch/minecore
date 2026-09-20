from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MineSiteCreate(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    status: str = Field(default="active", pattern="^(active|inactive|closed)$")
    location: str | None = Field(default=None, max_length=200)
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)


class MineSiteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    status: str | None = Field(default=None, pattern="^(active|inactive|closed)$")
    location: str | None = Field(default=None, max_length=200)
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)


class MineSiteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    name: str
    status: str
    location: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    created_at: datetime
    updated_at: datetime


class SiteAssignmentCreate(BaseModel):
    user_id: UUID


class SiteAssignmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    user_id: UUID
    mine_site_id: UUID
