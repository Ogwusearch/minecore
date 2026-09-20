"""Shared Pydantic base classes."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReadModel(ORMModel):
    id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime
