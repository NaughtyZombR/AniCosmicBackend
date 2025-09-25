from typing import Optional
from uuid import UUID

from core.models import AnimeMaterial, Genre, Post
from core.schemas.anime_material import AnimeMaterialCreate
from core.schemas.external.kodik import KodikMaterialData
from core.schemas.genre import GenreCreate
from core.schemas.post import PostCreate
from core.services.anime_material import AnimeMaterialService
from core.services.genre import GenreService
from core.services.kodik import KodikService
from core.services.post import PostService


class PostMaterialOrchestrator:
    """
    Оркестратор для создания Post вместе с AnimeMaterial через Kodik.
    Логика:
    1. Создаём Post.
    2. Получаем KodikMaterialData через KodikService.
    3. Преобразуем KodikMaterialData в AnimeMaterialCreate.
    4. Создаём AnimeMaterial и связываем с Post.
    5. Сохраняем всё разом.
    """

    def __init__(
        self,
        post_service: PostService,
        material_service: AnimeMaterialService,
        kodik_service: KodikService,
        genre_service: GenreService,
    ):
        self._post_service = post_service
        self._material_service = material_service
        self._kodik_service = kodik_service
        self._genre_service = genre_service

    async def create_post_with_material(
        self, schema: PostCreate, author_id: UUID
    ) -> tuple[Post, Optional[AnimeMaterial]]:
        """
        Создаёт Post и (опционально) AnimeMaterial.

        :param schema: PostCreate — данные для создания поста
        :param author_id: UUID автора поста
        :return: tuple[Post, AnimeMaterial | None]
        """
        # Создаём пост
        post = await self._post_service.create_post(schema, author_id)

        # Получаем данные из Kodik (KodikMaterialData)
        kodik_data: Optional[
            KodikMaterialData
        ] = await self._kodik_service.get_anime_material_data(schema.title)

        material: Optional[AnimeMaterial] = None
        if kodik_data:
            # Создаём или берём жанры из БД
            genres: list[Genre] = []
            if kodik_data.genres:
                for g_title in kodik_data.genres:
                    genre = await self._genre_service.get_by_title(g_title)
                    if not genre:
                        genre = await self._genre_service.create(
                            GenreCreate(title=g_title)
                        )
                    genres.append(genre)

            # Преобразуем KodikMaterialData в AnimeMaterialCreate
            material_schema = AnimeMaterialCreate(
                **kodik_data.model_dump(exclude={"genres"})
            )
            # Создаём материал и связываем с постом
            material = await self._material_service.create_material(
                material_schema, post.id, genres=genres
            )

            post.material = material  # привязываем к посту для сериализации

        # Сохраняем изменения в БД
        await self._post_service.save_changes()
        await self._material_service.save_changes()

        return post, material
