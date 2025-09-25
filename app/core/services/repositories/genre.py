from collections.abc import Sequence
from typing import override
from uuid import UUID

from core.models import Genre
from core.schemas.genre import GenreCreate, GenreUpdate
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository
from sqlalchemy import ColumnElement


class GenreRepository(SQLAlchemyRepository[Genre, GenreCreate, GenreUpdate]):
    @property
    def model_pk(self) -> UUID:
        return Genre.id

    @override
    @property
    def model(self) -> type[Genre]:
        return Genre

    @staticmethod
    def default_order_by() -> Sequence[ColumnElement]:
        return [Genre.created_at.desc()]

    async def get_by_title(self, title: str) -> Genre | None:
        return await self.get_one_where(where=[Genre.title == title])
