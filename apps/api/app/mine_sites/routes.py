from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import CurrentUser, get_current_user
from app.mine_sites.schemas import (
    MineSiteCreate,
    MineSiteRead,
    MineSiteUpdate,
    SiteAssignmentCreate,
    SiteAssignmentRead,
)
from app.mine_sites.service import MineSiteService

router = APIRouter(prefix="/mine-sites", tags=["mine-sites"])


@router.get("", response_model=list[MineSiteRead])
def list_mine_sites(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MineSiteService(db).list(current.organization_id)


@router.post("", response_model=MineSiteRead, status_code=status.HTTP_201_CREATED)
def create_mine_site(
    data: MineSiteCreate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MineSiteService(db).create(current.organization_id, data)


@router.get("/{site_id}", response_model=MineSiteRead)
def get_mine_site(
    site_id: UUID,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MineSiteService(db).get(current.organization_id, site_id)


@router.patch("/{site_id}", response_model=MineSiteRead)
def update_mine_site(
    site_id: UUID,
    data: MineSiteUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MineSiteService(db).update(current.organization_id, site_id, data)


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mine_site(
    site_id: UUID,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    MineSiteService(db).delete(current.organization_id, site_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ----------------------------------------------------------------------
# Assignments
# ----------------------------------------------------------------------
@router.get("/{site_id}/assignments", response_model=list[SiteAssignmentRead])
def list_assignments(
    site_id: UUID,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MineSiteService(db).list_assignments(current.organization_id, site_id)


@router.post(
    "/{site_id}/assignments",
    response_model=SiteAssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
def assign_user(
    site_id: UUID,
    data: SiteAssignmentCreate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MineSiteService(db).assign_user(current.organization_id, site_id, data)


@router.delete(
    "/{site_id}/assignments/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
def unassign_user(
    site_id: UUID,
    user_id: UUID,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    MineSiteService(db).unassign_user(current.organization_id, site_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
