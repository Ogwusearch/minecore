from app.core.crud_service import CrudService
from app.minerals.models import Mineral


class MineralService(CrudService[Mineral]):
    model = Mineral
    entity_name = "Mineral"


service = MineralService()
