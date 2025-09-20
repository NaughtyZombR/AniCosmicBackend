from uuid import UUID

from core.schemas.base import BaseSchema
from core.schemas.session import SessionRead
from core.schemas.user import UserRead


class LoginRead(SessionRead):
    user: UserRead


class TokenPayload(BaseSchema):
    sub: UUID
    iat: float
    exp: float
