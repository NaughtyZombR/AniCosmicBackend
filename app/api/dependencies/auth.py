from datetime import datetime, timezone
from typing import Annotated

from api.dependencies.services import AuthServiceDep, SessionServiceDep
from api.exceptions import auth as auth_exceptions
from core.models import Session
from core.schemas.auth import TokenPayload
from fastapi import Cookie, Depends
from fastapi.security import HTTPBearer
from starlette.requests import Request


# region Refresh token
async def get_refresh_token(
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> str:
    if refresh_token is None:
        raise auth_exceptions.NoRefreshTokenException()
    return refresh_token


RefreshTokenDep = Annotated[str, Depends(get_refresh_token)]


async def get_active_session(
    refresh_token: RefreshTokenDep,
    auth_service: AuthServiceDep,
    session_service: SessionServiceDep,
) -> Session:
    payload = auth_service.decode_jwt(refresh_token)
    session = await session_service.get_user_session(
        user_id=payload.sub,
        refresh_token=refresh_token,
    )

    if session is None:
        raise auth_exceptions.InvalidCredentialsException()
    if not session.is_active():
        raise auth_exceptions.RefreshTokenExpiredException()

    return session


ActiveSessionDep = Annotated[Session, Depends(get_active_session)]

# endregion
# region Access token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials = await super().__call__(request)
        if credentials is None:
            raise auth_exceptions.InvalidCredentialsException()
        return credentials.credentials


JWTBearerDep = Annotated[str, Depends(JWTBearer())]


async def get_active_access_token(
    token: JWTBearerDep,
    auth_service: AuthServiceDep,
) -> TokenPayload:
    payload = auth_service.decode_jwt(token)
    token_expires_at = datetime.fromtimestamp(payload.exp, tz=timezone.utc)

    if token_expires_at < datetime.now(timezone.utc):
        raise auth_exceptions.AccessTokenExpiredException()

    return payload


ValidBearerAccessToken = Annotated[
    TokenPayload, Depends(get_active_access_token)
]
