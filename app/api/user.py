from api.dependencies.pagination import PaginationQueryParams
from api.dependencies.services import UserServiceDep
from api.dependencies.user import Admin, UserQueryFilters, ValidUserId
from api.exceptions.user import (
    CantBanYourselfException,
    CantChangeRoleOfYourself,
)
from api.tags import APITags
from core.models import User
from core.schemas.user import (
    UserPaginationPageRead,
    UserRead,
    UsersBan,
    UserUpdateRole,
)
from core.services.repositories.pagination import ItemsPage
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=[APITags.User],
)


@router.get(
    "",
    response_model=UserPaginationPageRead,
)
async def get_all_users(
    query_filters: UserQueryFilters,
    pagination_params: PaginationQueryParams,
    user_service: UserServiceDep,
    _: Admin,
) -> ItemsPage[User]:
    users = await user_service.search_users(query_filters, pagination_params)
    return users


@router.patch(
    "/{user_id}/role",
    response_model=UserRead,
)
async def update_user_role(
    user: ValidUserId,
    schema: UserUpdateRole,
    user_service: UserServiceDep,
    admin: Admin,
) -> User:
    if user.id == admin.id:
        raise CantChangeRoleOfYourself()

    user = await user_service.update_by_id(user.id, schema)
    await user_service.save_changes()
    return user


@router.post("/ban")
async def ban_users(
    schema: UsersBan,
    user_service: UserServiceDep,
    admin: Admin,
) -> None:
    if admin.id in schema.ids:
        raise CantBanYourselfException()

    await user_service.ban_many(schema.ids)
    await user_service.save_changes()


@router.post(
    "/{user_id}/ban",
    response_model=UserRead,
)
async def ban_user(
    user: ValidUserId,
    user_service: UserServiceDep,
    admin: Admin,
) -> User:
    if admin.id == user.id:
        raise CantBanYourselfException()

    user = await user_service.ban(user)
    await user_service.save_changes()
    return user


@router.post(
    "/{user_id}/unban",
    response_model=UserRead,
)
async def unban_user(
    user: ValidUserId,
    user_service: UserServiceDep,
    _: Admin,
) -> User:
    user = await user_service.unban(user)
    await user_service.save_changes()
    return user


@router.post("/unban")
async def unban_users(
    schema: UsersBan,
    user_service: UserServiceDep,
    _: Admin,
) -> None:
    await user_service.unban_many(schema.ids)
    await user_service.save_changes()
