from __future__ import annotations

from functools import lru_cache
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import Settings


@lru_cache(maxsize=4)
def get_engine(database_url: str, pool_size: int, max_overflow: int, echo: bool) -> AsyncEngine:
    return create_async_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=pool_size,
        max_overflow=max_overflow,
        echo=echo,
    )


def get_sessionmaker(settings: Settings) -> async_sessionmaker[AsyncSession]:
    engine = get_engine(
        settings.database_url.get_secret_value(),
        settings.db_pool_size,
        settings.db_max_overflow,
        settings.db_echo,
    )
    return async_sessionmaker(engine, expire_on_commit=False)


async def session_scope(settings: Settings) -> AsyncIterator[AsyncSession]:
    session_factory = get_sessionmaker(settings)
    async with session_factory() as session:
        yield session

