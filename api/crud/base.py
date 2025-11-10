from typing import Any, List, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class CRUDBase:
    """Базовай класс методов обращения к БД."""

    def __init__(self, model: T) -> None:
        """Метод инициализации объектов."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[T]:
        """Получить объект по ID."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id,
            ),
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> List[T]:
        """Получить список всех объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in: Any, session: AsyncSession) -> T:
        """Создать объект и подгрузить отношения, если есть."""
        if hasattr(obj_in, "dict"):
            obj_in_data = obj_in.dict()
        elif isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = {}

        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()

        rels = [rel.key for rel in self.model.__mapper__.relationships]
        if rels:
            await session.refresh(db_obj, rels)
        else:
            await session.refresh(db_obj)

        return db_obj

    async def update(self, obj_id: int, obj_in: Any, session: AsyncSession) -> T:
        """Обновить объект и подгрузить отношения, если есть."""
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
            )
        db_obj = result.scalars().first()
        if not db_obj:
            return None

        if hasattr(obj_in, "dict"):
            update_data = obj_in.dict(exclude_unset=True)
        elif isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = {}

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()

        rels = [rel.key for rel in self.model.__mapper__.relationships]
        if rels:
            await session.refresh(db_obj, rels)
        else:
            await session.refresh(db_obj)

        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ) -> T:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
