from typing import Annotated
from uuid import UUID

from core.schemas.anime_material import (
    AnimeMaterialRead,
    AnimeMaterialReadShort,
)
from core.schemas.base import BaseSchema, NonEmptyString, TimestampSchema
from core.schemas.pagination import PaginationPageRead
from pydantic import Field

Title = Annotated[
    NonEmptyString,
    Field(
        description="Название поста",
        examples=["Новый пост"],
    ),
]


class _BasePost(BaseSchema):
    title: Title


class PostReadShort(_BasePost, TimestampSchema):
    id: UUID
    material: AnimeMaterialReadShort | None


class UserPostReadFull(PostReadShort):
    material: AnimeMaterialRead | None


class PostReadFull(UserPostReadFull):
    author_id: UUID


class PostCreate(_BasePost):
    pass


class PostUpdate(_BasePost):
    pass


class PostFilters(BaseSchema):
    title: NonEmptyString | None = None


PostPaginationPageRead = PaginationPageRead[PostReadShort]
