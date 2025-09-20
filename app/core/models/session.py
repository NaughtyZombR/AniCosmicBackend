import uuid
from datetime import datetime, timezone

from core.models.base import TimestampMixin
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class Session(TimestampMixin):
    refresh_token: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        CheckConstraint("expires_at > now() && expires_at > created_at"),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )

    def is_active(self) -> bool:
        return self.expires_at > datetime.now(tz=timezone.utc)
