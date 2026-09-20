from app.core.crud_service import CrudService
from app.material_types.models import MaterialType


class MaterialTypeService(CrudService[MaterialType]):
    model = MaterialType
    entity_name = "MaterialType"


service = MaterialTypeService()
