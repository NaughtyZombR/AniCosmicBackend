import uuid
from datetime import datetime, timedelta, timezone

import jwt
from api.exceptions import auth as auth_exceptions
from api.exceptions import user as user_exceptions
from core.models import User
from core.models.session import Session
from core.schemas.auth import TokenPayload
from core.schemas.user import UserLogin, UserRegister
from core.services.repositories.session import SessionRepository
from core.services.repositories.user import UserRepository
from pwdlib import PasswordHash
from settings.auth import AuthSettings
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, session: AsyncSession, settings: AuthSettings):
        self._user_repository = UserRepository(session)
        self._session_repository = SessionRepository(session)
        self._settings = settings
        self._pwd_context = PasswordHash.recommended()

    async def register(self, credentials: UserRegister) -> User:
        existing_user = await self._user_repository.get_by_email(
            credentials.email
        )
        if existing_user is not None:
            raise user_exceptions.UserAlreadyExistsException()

        user = User(
            email=credentials.email,
            hashed_password=self._pwd_context.hash(credentials.password),
        )
        user = await self._user_repository.create_from_orm(user)
        await self._user_repository.commit()
        return user

    async def login(self, credentials: UserLogin) -> tuple[User, Session]:
        user = await self._user_repository.get_by_email(credentials.email)
        if user is None:
            raise user_exceptions.UserNotFoundException()

        if user.is_banned:
            raise user_exceptions.UserIsBannedException()

        if not self._pwd_context.verify(
            credentials.password, user.hashed_password
        ):
            raise user_exceptions.UserInvalidPasswordException()

        session = Session(
            refresh_token=self.generate_refresh_token(user.id),
            user_id=user.id,
            expires_at=datetime.now(timezone.utc)
            + timedelta(
                seconds=self._settings.refresh_token_expiration_seconds,
            ),
        )
        await self._session_repository.create_from_orm(session)
        await self._session_repository.commit()
        return user, session

    async def refresh_session(self, session: Session) -> Session:
        new_session = Session(
            refresh_token=self.generate_refresh_token(session.user_id),
            user_id=session.user_id,
            expires_at=datetime.now(timezone.utc)
            + timedelta(
                seconds=self._settings.refresh_token_expiration_seconds,
            ),
        )
        await self._session_repository.delete_from_orm(session)
        await self._session_repository.create_from_orm(new_session)
        await self._session_repository.commit()

        return new_session

    def generate_access_token(self, user_id: uuid.UUID) -> str:
        expires_delta = timedelta(
            seconds=self._settings.access_token_expiration_seconds,
        )
        return self.encode_jwt(
            user_id=user_id,
            duration=expires_delta,
        )

    def generate_refresh_token(self, user_id: uuid.UUID) -> str:
        expires_delta = timedelta(
            seconds=self._settings.refresh_token_expiration_seconds,
        )
        return self.encode_jwt(
            user_id=user_id,
            duration=expires_delta,
        )

    def encode_jwt(
        self,
        user_id: uuid.UUID,
        duration: timedelta,
    ) -> str:
        now = datetime.now(timezone.utc)
        expires_at = now + duration
        payload = TokenPayload(
            sub=user_id,
            iat=now.timestamp(),
            exp=expires_at.timestamp(),
        )
        return jwt.encode(
            payload.model_dump(mode="json"),
            self._settings.jwt_secret_key.get_secret_value(),
            algorithm=self._settings.algorithm,
        )

    def decode_jwt(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(
                token,
                self._settings.jwt_secret_key.get_secret_value(),
                algorithms=self._settings.algorithm,
                options={"require": ["exp", "iat", "sub"]},
            )
            return TokenPayload(**payload)
        except jwt.PyJWTError as e:
            raise auth_exceptions.InvalidCredentialsException() from e
