from core.models.session import Session
from core.services.repositories.SQLAlchemy import SQLAlchemyRepository


class SessionRepository(SQLAlchemyRepository[Session, None, None]):
    @property
    def model(self) -> type[Session]:
        return Session

    @property
    def model_pk(self) -> str:
        return Session.refresh_token
