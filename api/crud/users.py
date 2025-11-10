from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.users import User


class UserCRUD(CRUDBase):

    async def get_by_tg_id(self, tg_id: int, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.tg_id == tg_id,
            ),
        )
        return db_obj.scalars().first()


user_crud = UserCRUD(User)
