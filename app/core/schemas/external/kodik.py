# core/schemas/external/kodik.py
from typing import Optional

from core.common.data.enums.kodik import MPAA, AnimeKind, MaterialStatus
from pydantic import BaseModel, Field, HttpUrl


class KodikMaterialData(BaseModel):
    """Данные материала, получаемые от Kodik API"""

    # Основные названия
    anime_title: Optional[str] = Field(None, description="Название аниме")
    title_en: Optional[str] = Field(None, description="Оригинальное название")
    other_titles: Optional[list[str]] = Field(
        None, description="Другие названия материала"
    )
    other_titles_en: Optional[list[str]] = None
    other_titles_jp: Optional[list[str]] = None

    # Лицензии
    anime_license_name: Optional[str] = None
    anime_licensed_by: Optional[list[str]] = None

    # Типы и статусы
    anime_kind: Optional[AnimeKind] = Field(
        None, description="Тип аниме (OVA, TV, Movie и т.д.)"
    )
    anime_status: Optional[MaterialStatus] = Field(
        None, description="Статус аниме"
    )
    drama_status: Optional[MaterialStatus] = None
    all_status: Optional[MaterialStatus] = None

    # Год / слоган / описание
    year: Optional[int] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    anime_description: Optional[str] = None

    # Медиа
    poster_url: Optional[HttpUrl] = None
    anime_poster_url: Optional[HttpUrl] = None
    drama_poster_url: Optional[HttpUrl] = None
    screenshots: Optional[list[HttpUrl]] = None

    # Хронометраж и страны
    duration: Optional[int] = None
    countries: Optional[list[str]] = None

    # Жанры / студии
    all_genres: Optional[list[str]] = None
    genres: Optional[list[str]] = None
    anime_genres: Optional[list[str]] = None
    drama_genres: Optional[list[str]] = None
    anime_studios: Optional[list[str]] = None

    # Рейтинги
    kinopoisk_rating: Optional[float] = None
    kinopoisk_votes: Optional[int] = None
    imdb_rating: Optional[float] = None
    imdb_votes: Optional[int] = None
    shikimori_rating: Optional[float] = None
    shikimori_votes: Optional[int] = None
    mydramalist_rating: Optional[float] = None
    mydramalist_votes: Optional[int] = None

    # Даты
    premiere_ru: Optional[str] = None
    premiere_world: Optional[str] = None
    aired_at: Optional[str] = None
    released_at: Optional[str] = None
    next_episode_at: Optional[str] = None

    # Ограничения
    rating_mpaa: Optional[MPAA] = Field(
        None, description="Возрастной рейтинг MPAA"
    )
    minimal_age: Optional[int] = None

    # Эпизоды
    episodes_total: Optional[int] = None
    episodes_aired: Optional[int] = None

    # Люди
    actors: Optional[list[str]] = None
    directors: Optional[list[str]] = None
    producers: Optional[list[str]] = None
    writers: Optional[list[str]] = None
    composers: Optional[list[str]] = None
    editors: Optional[list[str]] = None
    designers: Optional[list[str]] = None
    operators: Optional[list[str]] = None

    class Config:
        extra = "allow"  # на случай, если Kodik добавит новые поля
