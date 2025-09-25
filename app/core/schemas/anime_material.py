from datetime import date
from typing import Annotated, Optional
from uuid import UUID

from core.common.data.enums.kodik import MPAA, AnimeKind, MaterialStatus
from core.schemas.base import BaseSchema, NonEmptyString
from core.schemas.genre import GenreReadFull
from pydantic import (
    Field,
    HttpUrl,
    PlainSerializer,
)

Title = Annotated[
    NonEmptyString,
    Field(description="Название материала", examples=["Форма голоса"]),
]

CustomUrl = Annotated[
    HttpUrl,
    PlainSerializer(lambda value: value.unicode_string()),
]


class _BaseAnimeMaterial(BaseSchema):
    """Базовая схема AnimeMaterial, полностью соответствующая модели"""

    title: Title = Field(..., description="Название материала")
    anime_kind: Optional[AnimeKind] = Field(
        None, description="Тип аниме (OVA, TV, Movie и т.д.)"
    )
    episodes_total: Optional[int] = Field(
        None, description="Общее количество эпизодов"
    )
    episodes_aired: Optional[int] = Field(
        None, description="Количество вышедших эпизодов"
    )
    last_season: Optional[int] = Field(None, description="Последний сезон")
    duration: Optional[int] = Field(
        None, description="Длительность серии в минутах"
    )
    anime_status: Optional[MaterialStatus] = Field(
        None, description="Статус аниме"
    )
    rating_mpaa: Optional[MPAA] = Field(
        None, description="Возрастной рейтинг MPAA"
    )
    minimal_age: Optional[int] = Field(
        None, description="Минимальный возраст для просмотра"
    )
    description: Optional[str] = Field(None, description="Описание материала")
    premiere_world: Optional[date] = Field(
        None, description="Дата мировой премьеры"
    )
    premiere_ru: Optional[date] = Field(
        None, description="Дата премьеры в России"
    )
    poster_url: Optional[CustomUrl] = Field(
        None, description="URL постера аниме"
    )
    genres: Optional[list[GenreReadFull]] = Field(
        None, description="Список жанров"
    )


class AnimeMaterialCreate(_BaseAnimeMaterial):
    """Схема для создания материала (данные от Kodik)"""

    pass


class AnimeMaterialUpdate(_BaseAnimeMaterial):
    """Схема для обновления материала"""

    pass


class AnimeMaterialRead(_BaseAnimeMaterial):
    post_id: UUID = Field(
        ..., description="ID поста, к которому привязан материал"
    )


class AnimeMaterialReadShort(BaseSchema):
    title: Title = Field(..., description="Название материала")
    poster_url: Optional[CustomUrl] = Field(
        None, description="URL постера аниме"
    )
