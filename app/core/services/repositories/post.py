from collections.abc import Sequence
from typing import override
from uuid import UUID

from core.models import Post
from core.schemas.post import PostFilters, PostUpdate
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

    @staticmethod
    def default_order_by() -> Sequence[ColumnElement]:
        return [Post.created_at.desc()]

    async def get_posts_short(self) -> list[Post]:
        return await self.get_all(
            order_by=self.default_order_by(),
        )

    async def get_post_by_id_full(self, post_id: UUID) -> Post | None:
        return await self.get_one_where(
            where=[Post.id == post_id],
        )

    async def exists_by_title(self, title: str) -> bool:
        """Проверяет, есть ли пост с указанным названием"""
        result = await self.get_all(
            where=[Post.title == title],
        )
        return result.scalar() is not None

    @staticmethod
    def make_where_from_filters(
        filters: PostFilters,
    ) -> Sequence[ColumnElement[bool]]:
        where = []
        if filters.title is not None:
            where.append(Post.title.ilike(f"%{filters.title}%"))
        return where
