from uuid import UUID

from core.models import AnimeMaterial
from core.schemas.anime_material import AnimeMaterialCreate
from core.services.base import ModelService
from core.services.repositories.anime_material import AnimeMaterialRepository


class AnimeMaterialService(ModelService[AnimeMaterial, None, None]):
    @property
    def model_repository(self) -> type[AnimeMaterialRepository]:
        return AnimeMaterialRepository

    @property
    def not_found_error(self) -> type[Exception]:  # можно кастомный
        return Exception

    def __init__(self, session):
        super().__init__(session)

    async def create_material(
        self, schema: AnimeMaterialCreate, post_id: UUID
    ) -> AnimeMaterial:
        material_data = schema.model_dump()
        material = await self._repository.create_from_orm(
            AnimeMaterial(**material_data, post_id=post_id)
        )
        return material
