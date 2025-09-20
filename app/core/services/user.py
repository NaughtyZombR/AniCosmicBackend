from collections.abc import Sequence
from uuid import UUID

from api.exceptions.base import NotFoundException
from api.exceptions.user import (
    UserIsBannedException,
    UserIsNotBannedException,
    UserNotFoundException,
)
from core.models.user import User
from core.schemas.pagination import PaginationParams
from core.schemas.user import UserCreate, UserFilters
from core.services.base import ModelService
from core.services.repositories.pagination import ItemsPage
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository
from core.services.repositories.user import UserRepository


class UserService(ModelService[User, UserCreate, None]):
    @property
    def not_found_error(self) -> type[NotFoundException]:
        return UserNotFoundException

    @property
    def model_repository(self) -> type[SQLAlchemyRepository]:
        return UserRepository

    async def get_by_email(self, email: str) -> User | None:
        return await self._repository.get_by_email(email)

    async def search_users(
        self,
        filters: UserFilters,
        pagination_params: PaginationParams,
    ) -> ItemsPage[User]:
        where = self._repository.make_where_from_filters(filters)
        offset, limit = pagination_params.to_offset_limit()

        users = await self._repository.get_all(
            where=where,
            order_by=[User.created_at.desc()],
            offset=offset,
            limit=limit,
        )
        return ItemsPage(
            items=users,
            page=pagination_params.page,
            per_page=pagination_params.per_page,
            total=await self._repository.count(where=where),
        )

    async def ban(self, user: User) -> User:
        if user.is_banned:
            raise UserIsBannedException()

        user.is_banned = True
        await self._repository.update_from_orm(user)
        return user

    async def ban_many(self, user_ids: Sequence[UUID]) -> None:
        await self._repository.update_all_where(
            {"is_banned": True},
            where=[
                User.id.in_(user_ids),
            ],
        )

    async def unban(self, user: User) -> User:
        if not user.is_banned:
            raise UserIsNotBannedException()

        user.is_banned = False
        await self._repository.update_from_orm(user)
        return user

    async def unban_many(self, user_ids: Sequence[UUID]) -> None:
        await self._repository.update_all_where(
            {"is_banned": False},
            where=[
                User.id.in_(user_ids),
            ],
        )
