from typing import Annotated, Self
from uuid import UUID

from core.common.data.enums.user import UserRoles
from core.schemas.base import BaseSchema, NonEmptyString
from core.schemas.pagination import PaginationPageRead
from pydantic import AwareDatetime, EmailStr, Field, model_validator

Password = Annotated[
    NonEmptyString,
    Field(
        min_length=8,
        description="Пароль пользователя",
        examples=["password", "12345678"],
    ),
]


class _BaseUser(BaseSchema):
    email: EmailStr


class UserRead(_BaseUser):
    id: UUID
    role: UserRoles
    is_banned: bool
    created_at: AwareDatetime
    # is_verified: bool


UserPaginationPageRead = PaginationPageRead[UserRead]


class UserLogin(_BaseUser):
    password: Password


class UserRegister(UserLogin):
    pass


class UserCreate(UserRegister):
    pass


class UserUpdateEmail(BaseSchema):
    email: EmailStr


class UserUpdateRole(BaseSchema):
    role: UserRoles


class UserUpdatePassword(BaseSchema):
    password: Password
    new_password: Password

    @model_validator(mode="after")
    def verify_password(self) -> Self:
        if self.password != self.new_password:
            raise ValueError("Пароли не совпадают")
        return self


class UsersBan(BaseSchema):
    ids: set[UUID]


class UserFilters(BaseSchema):
    email: NonEmptyString | None = None
    role: UserRoles | None = None
    is_banned: bool | None = None
