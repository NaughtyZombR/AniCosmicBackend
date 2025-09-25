from typing import Annotated

from core.services.anime_material import AnimeMaterialService
from core.services.auth import AuthService
from core.services.email import EmailService
from core.services.genre import GenreService
from core.services.kodik import KodikService
from core.services.post import PostService
from core.services.session import SessionService
from core.services.user import UserService
from database import get_async_session
from fastapi import Depends
from settings.auth import auth_settings
from settings.kodik import kodik_settings
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


async def get_anime_material_service(
    session: AsyncSessionDep,
) -> AnimeMaterialService:
    return AnimeMaterialService(session)


async def get_genre_service(
    session: AsyncSessionDep,
) -> GenreService:
    return GenreService(session)


async def get_kodik_service() -> KodikService:
    return KodikService(kodik_settings)


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
AnimeMaterialServiceDep = Annotated[
    AnimeMaterialService, Depends(get_anime_material_service)
]
KodikServiceDep = Annotated[KodikService, Depends(get_kodik_service)]
GenreServiceDep = Annotated[GenreService, Depends(get_genre_service)]
SessionServiceDep = Annotated[SessionService, Depends(get_session_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
