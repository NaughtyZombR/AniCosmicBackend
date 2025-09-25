import uuid
from typing import TYPE_CHECKING

from core.common.data.enums.user import UserRoles
from core.models.base import TimestampMixin
from sqlalchemy import UUID, Boolean, Enum, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import Comment, Post


class User(TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    role: Mapped[UserRoles] = mapped_column(
        Enum(UserRoles, native_enum=False),
        default=UserRoles.USER,
        server_default=text("'USER'"),
        nullable=False,
    )
    is_banned: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
