from app.core.crud_router import make_crud_router
from app.pits import schemas
from app.pits.service import service

router = make_crud_router(
    service=service,
    prefix="/api/pits",
    tags=["pits"],
    schema_create=schemas.PitCreate,
    schema_update=schemas.PitUpdate,
    schema_read=schemas.PitRead,
    entity_label="Pit",
)
