from uuid import UUID

from api.exceptions.post import PostNotFoundException
from core.models import Post
from core.schemas.pagination import PaginationParams
from core.schemas.post import PostCreate, PostFilters, PostUpdate
from core.services.base import ModelService
from core.services.repositories.pagination import ItemsPage
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

    async def search_posts(
        self,
        filters: PostFilters,
        pagination_params: PaginationParams,
    ) -> ItemsPage[Post]:
        where = self._repository.make_where_from_filters(filters)
        offset, limit = pagination_params.to_offset_limit()

        posts = await self._repository.get_all(
            where=where,
            order_by=[Post.created_at.desc()],
            offset=offset,
            limit=limit,
        )
        return ItemsPage(
            items=posts,
            page=pagination_params.page,
            per_page=pagination_params.per_page,
            total=await self._repository.count(where=where),
        )

    async def get_all_posts_preview(self) -> list[Post]:
        # ToDo: Возвращать кратко, не всё наполнение
        return await self._repository.get_posts_short()

    async def get_full_post(self, post_id: UUID) -> Post:
        post = await self._repository.get_post_by_id_full(post_id)
        if post is None:
            raise self.not_found_error
        return post
