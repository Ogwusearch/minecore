from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Employee


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_in_org(self, organization_id: UUID) -> list[Employee]:
        stmt = (
            select(Employee)
            .where(Employee.organization_id == organization_id)
            .order_by(Employee.employee_number)
        )
        return list(self.db.scalars(stmt))

    def get_in_org(self, organization_id: UUID, employee_id: UUID) -> Employee | None:
        stmt = select(Employee).where(
            Employee.organization_id == organization_id,
            Employee.id == employee_id,
        )
        return self.db.scalars(stmt).first()

    def find_by_number(
        self, organization_id: UUID, employee_number: str
    ) -> Employee | None:
        stmt = select(Employee).where(
            Employee.organization_id == organization_id,
            Employee.employee_number == employee_number,
        )
        return self.db.scalars(stmt).first()

    def find_by_user(self, organization_id: UUID, user_id: UUID) -> Employee | None:
        stmt = select(Employee).where(
            Employee.organization_id == organization_id,
            Employee.user_id == user_id,
        )
        return self.db.scalars(stmt).first()
