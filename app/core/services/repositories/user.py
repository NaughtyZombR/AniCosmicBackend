from collections.abc import Sequence
from typing import override
from uuid import UUID

from core.models import User
from core.schemas.user import UserCreate, UserFilters
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository
from sqlalchemy import ColumnElement


class UserRepository(SQLAlchemyRepository[User, UserCreate, None]):
    @property
    def model_pk(self) -> UUID:
        return User.id

    @override
    @property
    def model(self) -> type[User]:
        return User

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_one_where(where=[User.email == email])

    @staticmethod
    def make_where_from_filters(
        filters: UserFilters,
    ) -> Sequence[ColumnElement[bool]]:
        where = []
        if filters.email is not None:
            where.append(User.email.ilike(f"%{filters.email}%"))
        if filters.is_banned is not None:
            where.append(User.is_banned == filters.is_banned)
        if filters.role is not None:
            where.append(User.role == filters.role)
        return where
