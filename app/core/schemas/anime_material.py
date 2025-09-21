from datetime import date
from typing import Annotated, Optional
from uuid import UUID

from core.schemas.base import BaseSchema, TimestampSchema
from pydantic import Field

Title = Annotated[
    str,
    Field(description="Название материала", examples=["Форма голоса"]),
]

Genre = Annotated[
    str,
    Field(
        description="Жанры через запятую", examples=["фэнтези, боевик, драма"]
    ),
]

Studio = Annotated[
    str,
    Field(
        description="Студия/продюсер через запятую", examples=["Studio Name"]
    ),
]


class _BaseAnimeMaterial(BaseSchema):
    title: Title
    type: Optional[str] = None
    episodes_count: Optional[int] = None
    genres: Optional[Genre] = None
    studio: Optional[Studio] = None
    mpaa_rating: Optional[str] = None
    age_limit: Optional[str] = None
    duration: Optional[int] = Field(None, description="Длительность в минутах")
    status: Optional[str] = None
    premiere_date: Optional[date] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None


class AnimeMaterialReadShort(_BaseAnimeMaterial, TimestampSchema):
    id: UUID


class AnimeMaterialReadFull(AnimeMaterialReadShort):
    post_id: UUID


class AnimeMaterialCreate(_BaseAnimeMaterial):
    pass


class AnimeMaterialUpdate(_BaseAnimeMaterial):
    pass
