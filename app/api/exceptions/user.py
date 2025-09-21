from api.exceptions.base import (
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from core.common.data.enums import UserRoles


class UserInvalidPasswordException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(detail="Invalid password")


class CantChangeRoleOfYourself(ForbiddenException):
    def __init__(self) -> None:
        super().__init__(detail="You can't change the role of yourself")


class UserIsBannedException(ForbiddenException):
    def __init__(self) -> None:
        super().__init__(detail="User is banned")


class UserIsNotBannedException(ForbiddenException):
    def __init__(self) -> None:
        super().__init__(detail="User is not banned")


class CantBanYourselfException(ForbiddenException):
    def __init__(self) -> None:
        super().__init__(detail="You can't ban yourself")


class UserNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(obj="User")


class UserAlreadyExistsException(ConflictException):
    def __init__(self) -> None:
        super().__init__(detail="User already exists")


class InvalidUserRoleException(ForbiddenException):
    def __init__(self, *required_roles: UserRoles) -> None:
        super().__init__(
            detail=f"User must have one of the following roles: "
            f"{', '.join(required_roles)}",
        )
