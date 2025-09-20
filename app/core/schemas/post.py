from datetime import time
from typing import Annotated
from uuid import UUID

from core.schemas.base import BaseSchema, NonEmptyString, TimestampSchema
from pydantic import Field, HttpUrl, PlainSerializer

from core.schemas.comment import CommentReadFull

Title = Annotated[
    NonEmptyString,
    Field(
        description="Название поста",
        examples=["Новый пост"],
    ),
]


def url_to_unicode_str(value: HttpUrl) -> str:
    return value.unicode_string()


CustomUrl = Annotated[
    HttpUrl,
    PlainSerializer(lambda value: value.unicode_string()),
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
    kodik_url: CustomUrl | None


class PostUpdate(_BasePost):
    pass
