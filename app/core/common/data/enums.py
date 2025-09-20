from enum import StrEnum, unique
from typing import Self


@unique
class UserRoles(StrEnum):
    ADMIN: str = "ADMIN"
    USER: str = "USER"
