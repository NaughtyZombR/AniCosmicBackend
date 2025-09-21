import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from core.models.base import TimestampMixin
from sqlalchemy import UUID, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import Post


class AnimeMaterial(TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )

    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    post: Mapped["Post"] = relationship(back_populates="material")

    title: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    episodes_count: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    genres: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # Через запятую
    studio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mpaa_rating: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age_limit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )  # мин.
    status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    premiere_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    poster_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
