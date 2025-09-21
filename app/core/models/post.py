import uuid
from datetime import time
from typing import TYPE_CHECKING, Optional

from core.models.base import TimestampMixin
from sqlalchemy import UUID, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import Comment, User


class Post(TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(String, nullable=False)

    kodik_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        default=None,
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    author: Mapped["User"] = relationship(back_populates="posts")

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
        lazy="joined",
    )
