from typing import Annotated, Optional
from uuid import UUID

from core.schemas.base import BaseSchema, NonEmptyString, TimestampSchema
from core.schemas.comment import CommentReadFull
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


class UserPostReadFull(PostReadShort):
    comments: list[CommentReadFull] | None


class PostReadFull(UserPostReadFull):
    author_id: UUID


class PostCreate(_BasePost):
    pass


class PostUpdate(_BasePost):
    pass
