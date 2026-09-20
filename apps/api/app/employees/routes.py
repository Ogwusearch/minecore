from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import CurrentUser, get_current_user
from app.employees.schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.employees.service import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=list[EmployeeRead])
def list_employees(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return EmployeeService(db).list(current.organization_id)


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    data: EmployeeCreate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return EmployeeService(db).create(current.organization_id, data)


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(
    employee_id: UUID,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return EmployeeService(db).get(current.organization_id, employee_id)


@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: UUID,
    data: EmployeeUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return EmployeeService(db).update(current.organization_id, employee_id, data)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: UUID,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    EmployeeService(db).delete(current.organization_id, employee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
