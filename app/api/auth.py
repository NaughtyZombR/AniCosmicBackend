from api.dependencies.auth import ActiveSessionDep
from api.dependencies.services import AuthServiceDep
from api.tags import APITags
from core.schemas.auth import LoginRead
from core.schemas.base import DictStrAny
from core.schemas.session import SessionRead
from core.schemas.user import UserLogin, UserRegister
from fastapi import APIRouter, Response, status

router = APIRouter(
    tags=[APITags.Auth],
)


@router.post(
    "/register",
    description="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    credentials: UserRegister,
    auth_service: AuthServiceDep,
) -> None:
    _ = await auth_service.register(credentials)


@router.post("/login", response_model=LoginRead)
async def login(
    response: Response,
    credentials: UserLogin,
    auth_service: AuthServiceDep,
) -> DictStrAny:
    user, session = await auth_service.login(credentials)

    response.set_cookie(
        key="refresh_token",
        value=session.refresh_token,
        httponly=True,
    )

    return {
        "access_token": auth_service.generate_access_token(session.user_id),
        "token_type": "Bearer",
        "user": user,
    }


@router.post("/refresh", response_model=SessionRead)
async def refresh(
    response: Response,
    auth_service: AuthServiceDep,
    active_session: ActiveSessionDep,
) -> DictStrAny:
    session = await auth_service.refresh_session(active_session)
    response.set_cookie(
        key="refresh_token",
        value=session.refresh_token,
        httponly=True,
    )
    return {
        "access_token": auth_service.generate_access_token(session.user_id),
        "token_type": "Bearer",
    }
