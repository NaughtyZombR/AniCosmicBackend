from typing import Literal

from core.schemas.base import BaseSchema


class SessionRead(BaseSchema):
    access_token: str
    token_type: Literal["Bearer"]
