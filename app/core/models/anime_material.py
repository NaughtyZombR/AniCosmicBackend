import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from core.models.base import TimestampMixin
from sqlalchemy import UUID, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import Genre, Post


class AnimeMaterial(TimestampMixin):
    __tablename__ = "anime_material"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )

    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    post: Mapped["Post"] = relationship(back_populates="material")

    title: Mapped[str] = mapped_column(String, nullable=False)
    anime_kind: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    episodes_total: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    episodes_aired: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    last_season: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    rating_mpaa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    minimal_age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    anime_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    premiere_world: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    premiere_ru: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    poster_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    genres: Mapped[list["Genre"]] = relationship(
        "Genre",
        secondary="anime_material_genres",  # Cм. genre.py
        back_populates="materials",
        lazy="selectin",
    )
