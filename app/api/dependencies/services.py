from typing import Annotated

from core.services.auth import AuthService
from core.services.email import EmailService
from core.services.post import PostService
from core.services.session import SessionService
from core.services.user import UserService
from database import get_async_session
from fastapi import Depends
from settings.auth import auth_settings
from sqlalchemy.ext.asyncio import AsyncSession

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_auth_service(
    session: AsyncSessionDep,
) -> AuthService:
    return AuthService(session, auth_settings)


async def get_email_service(
    session: AsyncSessionDep,
) -> EmailService:
    return EmailService(session)


async def get_post_service(
    session: AsyncSessionDep,
) -> PostService:
    return PostService(session)


async def get_session_service(
    session: AsyncSessionDep,
) -> SessionService:
    return SessionService(session)


async def get_user_service(
    session: AsyncSessionDep,
) -> UserService:
    return UserService(session)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
EmailServiceDep = Annotated[EmailService, Depends(get_email_service)]
PostServiceDep = Annotated[PostService, Depends(get_post_service)]
SessionServiceDep = Annotated[SessionService, Depends(get_session_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
