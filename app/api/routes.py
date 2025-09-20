from api.auth import router as auth_router
from api.email import router as email_router
from api.post import router as post_router
from api.misc import router as misc_router
from api.user import router as user_router
from core.schemas.error import internal_server_error
from fastapi import APIRouter

api_router = APIRouter(
    responses={
        **internal_server_error,
    }
)

api_router.include_router(auth_router)
api_router.include_router(email_router)
api_router.include_router(post_router)
api_router.include_router(misc_router)
api_router.include_router(user_router)
