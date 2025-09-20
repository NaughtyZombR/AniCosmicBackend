from collections.abc import Sequence
from typing import override
from uuid import UUID

from core.models import Post
from core.schemas.post import PostUpdate
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository
from sqlalchemy import ColumnElement


class PostRepository(SQLAlchemyRepository[Post, None, PostUpdate]):
    @property
    def model_pk(self) -> UUID:
        return Post.id

    @override
    @property
    def model(self) -> type[Post]:
        return Post

    async def get_posts_short(self) -> list[Post]:
        return await self.get_all(
            order_by=self.default_order_by(),
        )

    async def get_post_by_id_full(self, post_id: UUID) -> Post | None:
        return await self.get_one_where(
            where=[Post.id == post_id],
        )

    @staticmethod
    def default_order_by() -> Sequence[ColumnElement]:
        return [Post.created_at.desc()]
