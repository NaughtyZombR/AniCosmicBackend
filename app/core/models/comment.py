import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from core.models.base import TimestampMixin
from sqlalchemy import UUID, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import (
        Post,
        User
    )

class Comment(TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )

    author: Mapped["User"] = relationship(back_populates="comments")

    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
    )

    post: Mapped["Post"] = relationship(back_populates="comments")

