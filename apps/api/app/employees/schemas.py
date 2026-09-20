from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EmployeeCreate(BaseModel):
    employee_number: str = Field(min_length=1, max_length=50)
    full_name: str = Field(min_length=1, max_length=200)
    job_title: str | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    hire_date: date | None = None
    user_id: UUID | None = None


class EmployeeUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    job_title: str | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    hire_date: date | None = None
    status: str | None = Field(default=None, pattern="^(active|inactive|terminated)$")
    user_id: UUID | None = None


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    user_id: UUID | None
    employee_number: str
    full_name: str
    job_title: str | None
    department: str | None
    hire_date: date | None
    status: str
    created_at: datetime
    updated_at: datetime
