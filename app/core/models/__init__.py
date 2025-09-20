"""Все модели, что должны быть зарегистрированы при проведении миграции,
должны быть импортированы в этом файле."""

from .post import Post
from .comment import Comment
from .session import Session
from .smtp import SMTPConfig
from .user import User

__all__ = [
    "Post",
    "Comment",
    "Session",
    "SMTPConfig",
    "User",
]
