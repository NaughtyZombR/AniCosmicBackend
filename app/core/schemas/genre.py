from typing import Optional
from uuid import UUID

from core.schemas.base import BaseSchema, NonEmptyString
from pydantic import Field


class _BaseGenre(BaseSchema):
    title: NonEmptyString = Field(..., description="Название жанра")


class GenreReadShort(_BaseGenre):
    pass


class GenreReadFull(_BaseGenre):
    id: Optional[UUID] = Field(None, description="UUID жанра")


class GenreCreate(_BaseGenre):
    pass


class GenreUpdate(_BaseGenre):
    pass
