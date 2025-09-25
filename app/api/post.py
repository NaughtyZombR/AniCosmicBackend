from api.dependencies.pagination import PaginationQueryParams
from api.dependencies.post import PostQueryFilters, ValidPostId
from api.dependencies.services import (
    AnimeMaterialServiceDep,
    GenreServiceDep,
    KodikServiceDep,
    PostServiceDep,
)
from api.dependencies.user import Admin, UserOrAdmin
from api.tags import APITags
from core.models import Post
from core.schemas.post import (
    PostCreate,
    PostPaginationPageRead,
    PostReadShort,
    PostUpdate,
    UserPostReadFull,
)
from core.services.orchestrators.post_material import PostMaterialOrchestrator
from core.services.repositories.pagination import ItemsPage
from fastapi import APIRouter
from starlette import status

router = APIRouter(tags=[APITags.Post])


# region Post
@router.get("/posts", response_model=PostPaginationPageRead)
async def get_posts(
    query_filters: PostQueryFilters,
    pagination_params: PaginationQueryParams,
    post_service: PostServiceDep,
    _: UserOrAdmin,
) -> ItemsPage[Post]:
    posts = await post_service.search_posts(query_filters, pagination_params)
    return posts


@router.post("/posts/kodik", response_model=PostReadShort)
async def create_post_from_kodik(
    schema: PostCreate,
    admin: Admin,
    post_service: PostServiceDep,
    material_service: AnimeMaterialServiceDep,
    kodik_service: KodikServiceDep,
    genre_service: GenreServiceDep,
) -> Post:
    """
    Создаёт Post и AnimeMaterial по названию через Kodik
    """
    orchestrator = PostMaterialOrchestrator(
        post_service, material_service, kodik_service, genre_service
    )
    post, _ = await orchestrator.create_post_with_material(schema, admin.id)
    return post


@router.get("/posts/{post_id}", response_model=UserPostReadFull)
async def get_post(
    post: ValidPostId,
    _: UserOrAdmin,
) -> Post:
    return post


@router.post("/posts", response_model=PostReadShort)
async def create_post(
    post_service: PostServiceDep,
    schema: PostCreate,
    admin: Admin,
) -> Post:
    post = await post_service.create_post(schema=schema, author_id=admin.id)
    await post_service.save_changes()
    return post


@router.put("/posts/{post_id}", response_model=PostReadShort)
async def update_post(
    post: ValidPostId,
    schema: PostUpdate,
    post_service: PostServiceDep,
    _: Admin,
) -> Post:
    updated_post = await post_service.update_by_id(post.id, schema)
    await post_service.save_changes()
    return updated_post


@router.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post: ValidPostId,
    post_service: PostServiceDep,
    _: Admin,
) -> None:
    await post_service.delete_by_id(post.id)
    await post_service.save_changes()


# endregion
