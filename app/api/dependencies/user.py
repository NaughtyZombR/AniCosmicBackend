from typing import Annotated, Callable
from uuid import UUID

from api.dependencies.auth import ValidBearerAccessToken
from api.dependencies.services import UserServiceDep
from api.exceptions import user as user_exceptions
from core.common.data.enums.user import UserRoles
from core.models import User
from core.schemas.user import UserFilters
from fastapi import Depends

UserQueryFilters = Annotated[UserFilters, Depends(UserFilters)]


async def get_existing_user(
    user_id: UUID,
    user_service: UserServiceDep,
) -> User:
    return await user_service.get_by_id(user_id)


ValidUserId = Annotated[UUID, Depends(get_existing_user)]


async def get_current_user(
    token: ValidBearerAccessToken,
    user_service: UserServiceDep,
) -> User:
    return await user_service.get_by_id(token.sub)


AuthenticatedUser = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(
    user: AuthenticatedUser,
) -> User:
    if user.is_banned:
        raise user_exceptions.UserIsBannedException()

    return user


ActiveUser = Annotated[User, Depends(get_current_active_user)]


def get_user_with_role(*roles: UserRoles) -> Callable[[User], User]:
    def dependant(user: ActiveUser) -> User:
        if user.role not in roles:
            raise user_exceptions.InvalidUserRoleException(*roles)
        return user

    return dependant


USER = Annotated[User, Depends(get_user_with_role(UserRoles.USER))]

Admin = Annotated[User, Depends(get_user_with_role(UserRoles.ADMIN))]

UserOrAdmin = Annotated[
    User, Depends(get_user_with_role(UserRoles.USER, UserRoles.ADMIN))
]
