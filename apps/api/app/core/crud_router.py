"""Generic CRUD router factory.

Produces the five standard endpoints for any CrudService subclass:

    GET    {prefix}            list
    POST   {prefix}            create
    GET    {prefix}/{id}       read
    PATCH  {prefix}/{id}       update
    DELETE {prefix}/{id}       delete

IMPORTANT: this module must NOT use `from __future__ import annotations`.
FastAPI resolves the payload type at registration time by inspecting the
function signature; string annotations would resolve against the module
globals, where `schema_create` does not exist (it is a parameter of the
factory). That would cause FastAPI to treat the body as a query parameter.
"""
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.crud_service import ConflictError, CrudService, ReferenceError
from app.core.dependencies import current_organization_id
from app.db.session import get_db


def make_crud_router(
    *,
    service: CrudService,
    prefix: str,
    tags: list,
    schema_create: type,
    schema_update: type,
    schema_read: type,
    entity_label: str,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    @router.get("", response_model=list[schema_read])
    def list_items(
        org_id: UUID = Depends(current_organization_id),
        db: Session = Depends(get_db),
    ) -> Any:
        return service.list_for_org(db, org_id)

    @router.post("", response_model=schema_read, status_code=status.HTTP_201_CREATED)
    def create_item(
        payload: schema_create,
        org_id: UUID = Depends(current_organization_id),
        db: Session = Depends(get_db),
    ) -> Any:
        try:
            return service.create(db, org_id, payload)
        except ConflictError as exc:
            raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
        except ReferenceError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    @router.get("/{item_id}", response_model=schema_read)
    def get_item(
        item_id: UUID,
        org_id: UUID = Depends(current_organization_id),
        db: Session = Depends(get_db),
    ) -> Any:
        item = service.get(db, org_id, item_id)
        if item is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"{entity_label} not found")
        return item

    @router.patch("/{item_id}", response_model=schema_read)
    def update_item(
        item_id: UUID,
        payload: schema_update,
        org_id: UUID = Depends(current_organization_id),
        db: Session = Depends(get_db),
    ) -> Any:
        try:
            item = service.update(db, org_id, item_id, payload)
        except ConflictError as exc:
            raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
        except ReferenceError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
        if item is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"{entity_label} not found")
        return item

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(
        item_id: UUID,
        org_id: UUID = Depends(current_organization_id),
        db: Session = Depends(get_db),
    ) -> None:
        if not service.delete(db, org_id, item_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"{entity_label} not found")
        return None

    return router
