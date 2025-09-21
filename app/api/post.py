from api.dependencies.post import ValidPostId
from api.dependencies.services import (
    PostServiceDep,
)
from api.dependencies.user import UserOrAdmin
from api.tags import APITags
from core.models import Post
from core.schemas.post import (
    PostCreate,
    PostReadFull,
    PostReadShort,
    PostUpdate,
)
from fastapi import APIRouter
from starlette import status

router = APIRouter(tags=[APITags.Post])


# region Post
@router.get("/posts", response_model=list[PostReadShort])
async def get_all_posts(
    post_service: PostServiceDep,
    _: UserOrAdmin,
) -> list[Post]:
    posts = await post_service.get_all_posts_preview()
    return posts


@router.get("/posts/{post_id}", response_model=PostReadFull)
async def get_post(
    post: ValidPostId,
    post_service: PostServiceDep,
    _: UserOrAdmin,
) -> Post:
    post = await post_service.get_full_post(post.id)
    return post


@router.post("/posts", response_model=PostReadFull)
async def create_post(
    post_service: PostServiceDep,
    schema: PostCreate,
    user: UserOrAdmin,
) -> Post:
    post = await post_service.create_post(schema=schema, author_id=user.id)
    await post_service.save_changes()
    return post


@router.put("/posts/{post_id}", response_model=PostReadShort)
async def update_post(
    post: ValidPostId,
    schema: PostUpdate,
    post_service: PostServiceDep,
    _: UserOrAdmin,
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
    _: UserOrAdmin,
) -> None:
    await post_service.delete_by_id(post.id)
    await post_service.save_changes()


# endregion
