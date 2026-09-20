from app.core.crud_router import make_crud_router
from app.minerals import schemas
from app.minerals.service import service

router = make_crud_router(
    service=service,
    prefix="/api/minerals",
    tags=["minerals"],
    schema_create=schemas.MineralCreate,
    schema_update=schemas.MineralUpdate,
    schema_read=schemas.MineralRead,
    entity_label="Mineral",
)
