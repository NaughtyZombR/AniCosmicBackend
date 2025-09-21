import logging
from uuid import UUID, uuid4

from core.models import AnimeMaterial, Post
from core.schemas.post import PostCreate
from core.services.gateways.kodik import KodikGateway
from core.services.repositories.anime_material import AnimeMaterialRepository
from core.services.repositories.post import PostRepository

logger = logging.getLogger(__name__)


class KodikService:
    def __init__(
        self,
        gateway: KodikGateway,
        post_repository: PostRepository,
        material_repository: AnimeMaterialRepository,
    ):
        self._gateway = gateway
        self._post_repository = post_repository
        self._material_repository = material_repository

    async def get_anime_by_title(self, title: str) -> dict:
        """Возвращает JSON с материалом и эпизодами для конкретного названия"""
        data = await self._gateway.search_by_title(title)
        results = data.get("results", [])
        return results[0] if results else {}

    async def create_post_with_material(
        self, schema: PostCreate, author_id: UUID
    ) -> tuple[Post, AnimeMaterial]:
        """Создаёт один пост + материал по названию через репозитории"""
        post = await self._post_repository.create_from_orm(
            Post(id=uuid4(), title=schema.title, author_id=author_id)
        )

        material_json = await self.get_anime_by_title(schema.title)
        material_data = material_json.get("material_data", {})

        material = await self._material_repository.create_from_orm(
            AnimeMaterial(
                id=uuid4(),
                post_id=post.id,
                title=material_data.get("title") or schema.title,
                type=material_json.get("type"),
                episodes_count=material_json.get("episodes_count"),
                genres=",".join(material_data.get("genres", []))
                if material_data.get("genres")
                else None,
                studio=",".join(material_data.get("producers", []))
                if material_data.get("producers")
                else None,
                duration=material_data.get("duration"),
                description=material_data.get("description"),
                premiere_date=material_data.get("premiere_ru"),
                poster_url=material_data.get("poster_url"),
            )
        )

        return post, material

    async def import_all_content(
        self, author_id: UUID
    ) -> list[tuple[Post, AnimeMaterial]]:
        added = []
        next_page: str | None = None

        while True:
            data = await self._gateway.list_content(next_page)
            results = data.get("results", [])

            for item in results:
                title = item.get("title")
                if not title:
                    continue

                exists = await self._post_repository.exists_by_title(title)
                if exists:
                    continue

                try:
                    post = await self._post_repository.create_from_orm(
                        Post(id=uuid4(), title=title, author_id=author_id)
                    )

                    material_data = item.get("material_data", {})
                    material = await self._material_repository.create_from_orm(
                        AnimeMaterial(
                            id=uuid4(),
                            post_id=post.id,
                            title=material_data.get("title") or title,
                            type=item.get("type"),
                            episodes_count=item.get("episodes_count"),
                            genres=",".join(material_data.get("genres", []))
                            if material_data.get("genres")
                            else None,
                            studio=",".join(material_data.get("producers", []))
                            if material_data.get("producers")
                            else None,
                            duration=material_data.get("duration"),
                            description=material_data.get("description"),
                            premiere_date=material_data.get("premiere_ru"),
                            poster_url=material_data.get("poster_url"),
                        )
                    )

                    added.append((post, material))
                except Exception as e:
                    logger.error("Ошибка при добавлении %s: %s", title, e)
                    continue

            next_page = data.get("next_page")
            if not next_page:
                break

        return added
