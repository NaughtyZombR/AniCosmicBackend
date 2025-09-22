from uuid import UUID

from core.schemas.post import PostCreate
from core.services.anime_material import AnimeMaterialService
from core.services.kodik import KodikService
from core.services.post import PostService


class PostMaterialOrchestrator:
    def __init__(
        self,
        post_service: PostService,
        material_service: AnimeMaterialService,
        kodik_service: KodikService,
    ):
        self._post_service = post_service
        self._material_service = material_service
        self._kodik_service = kodik_service

    async def create_post_with_material(
        self, schema: PostCreate, author_id: UUID
    ):
        # Создаём пост
        post = await self._post_service.create_post(schema, author_id)
        # Получаем Pydantic-схему материала
        material_schema = await self._kodik_service.get_anime_material_schema(
            schema.title
        )

        # Если Kodik вернул данные, создаём AnimeMaterial
        if material_schema:
            material = await self._material_service.create_material(
                material_schema, post.id
            )
        else:
            material = None

        # Сохраняем всё разом
        await self._post_service.save_changes()
        await self._material_service.save_changes()

        return post, material
