from typing import Annotated

from api.tags import APITags
from core.schemas.misc import HealthCheckRead
from database import get_async_session
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

router = APIRouter(
    tags=[APITags.Misc],
)


@router.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@router.get("/health", response_model=HealthCheckRead)
async def health_check(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    try:
        db_ping = (await db_session.execute(select(1))).scalar()
    except (OSError, InterfaceError):
        db_ping = False

    return {
        "database": db_ping,
    }
