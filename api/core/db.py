from typing import AsyncGenerator


from fastapi import HTTPException
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column as mp

from core.config import settings


class PreBase:
    """Базовый класс для всех моделей."""

    id: Mapped[int] = mp(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator:
    """Асинхронный генератор сессий."""
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
            await async_session.commit()
        except HTTPException as http_exc:
            await async_session.rollback()
            raise http_exc
        except Exception as err:
            await async_session.rollback()
            raise HTTPException(status_code=500, detail=str(err))
