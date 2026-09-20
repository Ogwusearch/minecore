"""Mining operation endpoints.

Standard CRUD plus the three workflow transitions:

    POST /api/mining-operations/{id}/record
    POST /api/mining-operations/{id}/approve
    POST /api/mining-operations/{id}/cancel

And a read-only audit trail:

    GET  /api/mining-operations/{id}/audit
"""
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.audit.schemas import AuditLogRead
from app.audit.service import list_for_entity
from app.core.crud_service import ConflictError, ReferenceError
from app.core.dependencies import current_organization_id, current_user_id
from app.db.session import get_db
from app.mining import schemas
from app.mining.service import ENTITY_TYPE, service
from app.mining.workflow import WorkflowError

router = APIRouter(prefix="/api/mining-operations", tags=["mining-operations"])


# -----------------------------------------------------------------
# Read
# -----------------------------------------------------------------

@router.get("", response_model=list[schemas.MiningOperationRead])
def list_operations(
    org_id: UUID = Depends(current_organization_id),
    db: Session = Depends(get_db),
    status_filter: str | None = Query(default=None, alias="status"),
    mine_site_id: UUID | None = None,
    pit_id: UUID | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
):
    return service.list_for_org(
        db,
        org_id,
        status=status_filter,
        mine_site_id=mine_site_id,
        pit_id=pit_id,
        from_date=from_date,
        to_date=to_date,
    )


@router.get("/{op_id}", response_model=schemas.MiningOperationRead)
def get_operation(
    op_id: UUID,
    org_id: UUID = Depends(current_organization_id),
    db: Session = Depends(get_db),
):
    op = service.get(db, org_id, op_id)
    if op is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MiningOperation not found")
    return op


@router.get("/{op_id}/audit", response_model=list[AuditLogRead])
def get_operation_audit(
    op_id: UUID,
    org_id: UUID = Depends(current_organization_id),
    db: Session = Depends(get_db),
):
    op = service.get(db, org_id, op_id)
    if op is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MiningOperation not found")
    return list_for_entity(
        db,
        organization_id=org_id,
        entity_type=ENTITY_TYPE,
        entity_id=op.id,
    )


# -----------------------------------------------------------------
# Create
# -----------------------------------------------------------------

@router.post(
    "",
    response_model=schemas.MiningOperationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_operation(
    payload: schemas.MiningOperationCreate,
    org_id: UUID = Depends(current_organization_id),
    user_id: UUID = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    try:
        return service.create(db, org_id, user_id, payload)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except ReferenceError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc


# -----------------------------------------------------------------
# Update / Delete
# -----------------------------------------------------------------

@router.patch("/{op_id}", response_model=schemas.MiningOperationRead)
def update_operation(
    op_id: UUID,
    payload: schemas.MiningOperationUpdate,
    org_id: UUID = Depends(current_organization_id),
    user_id: UUID = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    try:
        op = service.update(db, org_id, user_id, op_id, payload)
    except WorkflowError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except ReferenceError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    if op is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MiningOperation not found")
    return op


@router.delete("/{op_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operation(
    op_id: UUID,
    org_id: UUID = Depends(current_organization_id),
    user_id: UUID = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    try:
        ok = service.delete(db, org_id, user_id, op_id)
    except WorkflowError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MiningOperation not found")
    return None


# -----------------------------------------------------------------
# Workflow transitions
# -----------------------------------------------------------------

@router.post("/{op_id}/record", response_model=schemas.MiningOperationRead)
def record_operation(
    op_id: UUID,
    org_id: UUID = Depends(current_organization_id),
    user_id: UUID = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    try:
        op = service.record(db, org_id, user_id, op_id)
    except WorkflowError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    if op is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MiningOperation not found")
    return op


@router.post("/{op_id}/approve", response_model=schemas.MiningOperationRead)
def approve_operation(
    op_id: UUID,
    org_id: UUID = Depends(current_organization_id),
    user_id: UUID = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    try:
        op = service.approve(db, org_id, user_id, op_id)
    except WorkflowError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    if op is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MiningOperation not found")
    return op


@router.post("/{op_id}/cancel", response_model=schemas.MiningOperationRead)
def cancel_operation(
    op_id: UUID,
    payload: schemas.CancelRequest,
    org_id: UUID = Depends(current_organization_id),
    user_id: UUID = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    try:
        op = service.cancel(db, org_id, user_id, op_id, payload.reason)
    except WorkflowError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    if op is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MiningOperation not found")
    return op
