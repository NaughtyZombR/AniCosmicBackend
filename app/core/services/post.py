from datetime import time
from uuid import UUID

from api.exceptions.post import PostNotFoundException
from core.models import Post
from core.schemas.post import PostCreate, PostUpdate
from core.services.base import ModelService
from core.services.repositories.post import PostRepository


class PostService(ModelService[Post, None, PostUpdate]):
    @property
    def model_repository(self) -> type[PostRepository]:
        return PostRepository

    @property
    def not_found_error(self) -> type[PostNotFoundException]:
        return PostNotFoundException

    def __init__(self, session):
        super().__init__(session)

    async def create_post(self, schema: PostCreate, author_id: UUID) -> Post:
        post_data = schema.model_dump()
        post = await self._repository.create_from_orm(
            Post(
                **post_data,
                author_id=author_id,
            )
        )
        return post

    async def get_all_posts_preview(self) -> list[Post]:
        # ToDo: Возвращать кратко, не всё наполнение
        return await self._repository.get_posts_short()


    async def get_full_post(self, post_id: UUID) -> Post:
        post = await self._repository.get_post_by_id_full(post_id)
        if post is None:
            raise self.not_found_error
        return post
