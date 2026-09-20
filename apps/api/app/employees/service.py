from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.employees.repository import EmployeeRepository
from app.employees.schemas import EmployeeCreate, EmployeeUpdate
from app.models import Employee


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = EmployeeRepository(db)

    def list(self, organization_id: UUID) -> list[Employee]:
        return self.repo.list_in_org(organization_id)

    def get(self, organization_id: UUID, employee_id: UUID) -> Employee:
        emp = self.repo.get_in_org(organization_id, employee_id)
        if emp is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")
        return emp

    def create(self, organization_id: UUID, data: EmployeeCreate) -> Employee:
        if self.repo.find_by_number(organization_id, data.employee_number) is not None:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Employee number '{data.employee_number}' already exists",
            )

        if data.user_id is not None:
            existing = self.repo.find_by_user(organization_id, data.user_id)
            if existing is not None:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    "This user is already linked to an employee record",
                )

        emp = Employee(
            organization_id=organization_id,
            employee_number=data.employee_number,
            full_name=data.full_name,
            job_title=data.job_title,
            department=data.department,
            hire_date=data.hire_date,
            user_id=data.user_id,
            status="active",
        )
        self.db.add(emp)
        self.db.flush()
        self.db.refresh(emp)
        return emp

    def update(
        self, organization_id: UUID, employee_id: UUID, data: EmployeeUpdate
    ) -> Employee:
        emp = self.get(organization_id, employee_id)

        if data.user_id is not None and data.user_id != emp.user_id:
            clash = self.repo.find_by_user(organization_id, data.user_id)
            if clash is not None and clash.id != emp.id:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    "This user is already linked to another employee record",
                )
            emp.user_id = data.user_id

        for field in ("full_name", "job_title", "department", "hire_date", "status"):
            value = getattr(data, field)
            if value is not None:
                setattr(emp, field, value)

        self.db.flush()
        self.db.refresh(emp)
        return emp

    def delete(self, organization_id: UUID, employee_id: UUID) -> None:
        emp = self.get(organization_id, employee_id)
        self.db.delete(emp)
