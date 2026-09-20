from app.core.crud_router import make_crud_router
from app.material_types import schemas
from app.material_types.service import service

router = make_crud_router(
    service=service,
    prefix="/api/material-types",
    tags=["material-types"],
    schema_create=schemas.MaterialTypeCreate,
    schema_update=schemas.MaterialTypeUpdate,
    schema_read=schemas.MaterialTypeRead,
    entity_label="MaterialType",
)
