from uuid import UUID

from api.exceptions.anime_material import AnimeMaterialNotFoundException
from core.models import AnimeMaterial, Genre
from core.schemas.anime_material import AnimeMaterialCreate
from core.services.base import ModelService
from core.services.repositories.anime_material import AnimeMaterialRepository
from core.services.repositories.genre import GenreRepository
from sqlalchemy.ext.asyncio import AsyncSession


class AnimeMaterialService(ModelService[AnimeMaterial, None, None]):
    @property
    def model_repository(self) -> type[AnimeMaterialRepository]:
        return AnimeMaterialRepository

    @property
    def not_found_error(self) -> type[Exception]:
        return AnimeMaterialNotFoundException

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self._genre_repo = GenreRepository(session)

    async def create_material(
        self,
        schema: AnimeMaterialCreate,
        post_id: UUID,
        genres: list[Genre] = None,
    ) -> AnimeMaterial:
        material_data = schema.model_dump(exclude={"genres"})
        material = AnimeMaterial(**material_data, post_id=post_id)

        # Присваиваем переданные объекты жанров
        material.genres = genres or []

        # Создаём материал
        material = await self._repository.create_from_orm(material)
        return material
