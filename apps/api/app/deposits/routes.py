from app.core.crud_router import make_crud_router
from app.deposits import schemas
from app.deposits.service import service

router = make_crud_router(
    service=service,
    prefix="/api/deposits",
    tags=["deposits"],
    schema_create=schemas.DepositCreate,
    schema_update=schemas.DepositUpdate,
    schema_read=schemas.DepositRead,
    entity_label="Deposit",
)
