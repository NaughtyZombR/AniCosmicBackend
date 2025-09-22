from datetime import date
from typing import Annotated, Optional
from uuid import UUID

from core.schemas.base import BaseSchema, NonEmptyString
from pydantic import (
    Field,
    HttpUrl,
    PlainSerializer,
    field_validator,
    model_validator,
)

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

CustomUrl = Annotated[
    HttpUrl,
    PlainSerializer(lambda value: value.unicode_string()),
]


class _BaseAnimeMaterial(BaseSchema):
    title: NonEmptyString = Field(..., description="Название аниме")
    type: str | None = Field(None, description="Тип аниме")
    episodes_count: int | None = Field(
        None, description="Общее количество серий"
    )
    released_episodes_count: int | None = Field(
        None, description="Вышедших серий"
    )
    last_season: int | None = Field(None, description="Последний сезон")
    genres: str | None = Field(None, description="Жанры через запятую")
    studio: str | None = Field(
        None, description="Студия / продюсеры через запятую"
    )
    duration: int | None = Field(
        None, description="Длительность серии в минутах"
    )
    description: str | None = Field(None, description="Описание")
    premiere_date: date | None = Field(None, description="Дата премьеры")
    poster_url: CustomUrl | None = Field(None, description="URL постера")


class AnimeMaterialRead(_BaseAnimeMaterial):
    post_id: UUID


class AnimeMaterialCreate(_BaseAnimeMaterial):
    """Схема для создания материала (входные данные от API Kodik)"""

    # Временные поля, которые приходят только от внешнего API
    episodes_total: Optional[int] = Field(None, exclude=True)
    episodes_aired: Optional[int] = Field(None, exclude=True)
    anime_poster_url: Optional[str] = Field(None, exclude=True)

    @field_validator("genres", mode="before")
    def join_genres(cls, v):
        if isinstance(v, list):
            return ",".join(v)
        return v

    @field_validator("studio", mode="before")
    def join_studio(cls, v):
        if isinstance(v, list):
            return ",".join(v)
        return v

    @model_validator(mode="before")
    def normalize_fields(cls, data: dict):
        """Приводим данные API к нашему формату"""
        if "episodes_total" in data and "episodes_count" not in data:
            data["episodes_count"] = data["episodes_total"]

        if "episodes_aired" in data and "released_episodes_count" not in data:
            data["released_episodes_count"] = data["episodes_aired"]

        if "poster_url" not in data and "anime_poster_url" in data:
            data["poster_url"] = data["anime_poster_url"]

        return data


class AnimeMaterialUpdate(_BaseAnimeMaterial):
    pass
