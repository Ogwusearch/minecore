from app.core.crud_router import make_crud_router
from app.materials import schemas
from app.materials.service import service

router = make_crud_router(
    service=service,
    prefix="/api/materials",
    tags=["materials"],
    schema_create=schemas.MaterialCreate,
    schema_update=schemas.MaterialUpdate,
    schema_read=schemas.MaterialRead,
    entity_label="Material",
)
