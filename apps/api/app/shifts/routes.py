from app.core.crud_router import make_crud_router
from app.shifts import schemas
from app.shifts.service import service

router = make_crud_router(
    service=service,
    prefix="/api/shifts",
    tags=["shifts"],
    schema_create=schemas.ShiftCreate,
    schema_update=schemas.ShiftUpdate,
    schema_read=schemas.ShiftRead,
    entity_label="Shift",
)
