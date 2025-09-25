import uuid
from typing import TYPE_CHECKING

from core.models.base import TimestampMixin
from sqlalchemy import UUID, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import AnimeMaterial


# связующая таблица
anime_material_genres = Table(
    "anime_material_genres",
    TimestampMixin.metadata,
    Column(
        "material_id",
        UUID,
        ForeignKey("anime_material.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "genre_id",
        UUID,
        ForeignKey("genre.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Genre(TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    materials: Mapped[list["AnimeMaterial"]] = relationship(
        "AnimeMaterial",
        secondary=anime_material_genres,
        back_populates="genres",
        lazy="selectin",
    )
