from collections.abc import AsyncGenerator

from settings.database import db_settings
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_async_engine(db_settings.url, pool_recycle=60 * 60)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
