from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import CurrentUser, get_current_user
from app.organizations.schemas import OrganizationRead, OrganizationUpdate
from app.organizations.service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/current", response_model=OrganizationRead)
def get_current_organization(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return OrganizationService(db).get_current(current.organization_id)


@router.patch("/current", response_model=OrganizationRead)
def update_current_organization(
    data: OrganizationUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return OrganizationService(db).update(current.organization_id, data)
