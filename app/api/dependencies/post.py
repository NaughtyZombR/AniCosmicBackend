import uuid
from typing import Annotated

from api.dependencies.services import PostServiceDep
from core.models import Post
from fastapi import Depends


async def get_existing_post(
    post_id: uuid.UUID,
    post_service: PostServiceDep,
) -> Post:
    return await post_service.get_by_id(post_id)


ValidPostId = Annotated[Post, Depends(get_existing_post)]
