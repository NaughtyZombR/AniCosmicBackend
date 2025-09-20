from typing import Annotated
from uuid import UUID

from core.schemas.base import BaseSchema, NonEmptyString
from pydantic import Field

Text = Annotated[
    NonEmptyString,
    Field(
        description="Содержание комментария",
        examples=["Новый комментарий"],
    ),
]

class _BaseComment(BaseSchema):
    text: Text

class UserCommentRead(_BaseComment):
    pass

class CommentReadFull(UserCommentRead):
    author_id: UUID


class CommentCreate(_BaseComment):
    text: Text


class CommentUpdate(_BaseComment):
    pass
