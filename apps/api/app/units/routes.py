from app.core.crud_router import make_crud_router
from app.units import schemas
from app.units.service import service

router = make_crud_router(
    service=service,
    prefix="/api/units",
    tags=["units"],
    schema_create=schemas.UnitCreate,
    schema_update=schemas.UnitUpdate,
    schema_read=schemas.UnitRead,
    entity_label="Unit",
)
