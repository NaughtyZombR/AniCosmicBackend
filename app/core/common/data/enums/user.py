from enum import StrEnum, unique


@unique
class UserRoles(StrEnum):
    ADMIN: str = "ADMIN"
    USER: str = "USER"
