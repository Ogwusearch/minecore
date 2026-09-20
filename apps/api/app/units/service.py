from app.core.crud_service import CrudService
from app.units.models import Unit


class UnitService(CrudService[Unit]):
    model = Unit
    entity_name = "Unit"


service = UnitService()
