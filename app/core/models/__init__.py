"""Все модели, что должны быть зарегистрированы при проведении миграции,
должны быть импортированы в этом файле."""

from .anime_material import AnimeMaterial
from .comment import Comment
from .genre import Genre
from .post import Post
from .session import Session
from .smtp import SMTPConfig
from .user import User

__all__ = [
    "Post",
    "Comment",
    "Session",
    "SMTPConfig",
    "User",
    "AnimeMaterial",
    "Genre",
]
