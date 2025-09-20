import uuid

from api.exceptions.auth import InvalidCredentialsException
from api.exceptions.base import NotFoundException
from core.models import Session
from core.services.base import ModelService
from core.services.repositories.session import SessionRepository
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository


class SessionService(ModelService[Session, None, None]):
    @property
    def model_repository(self) -> type[SQLAlchemyRepository]:
        return SessionRepository

    @property
    def not_found_error(self) -> type[NotFoundException]:
        return InvalidCredentialsException  # noqa

    async def get_user_session(
        self,
        *,
        user_id: uuid.UUID,
        refresh_token: str,
    ) -> Session | None:
        session = await self._repository.get_one_where(
            where=[
                Session.user_id == user_id,
                Session.refresh_token == refresh_token,
            ],
        )
        return session
