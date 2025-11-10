from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import SubjectEnum
from crud.base import CRUDBase
from models.scores import Score


class ScoreCRUD(CRUDBase):

    async def get_by_user_id(self, user_id: int, session: AsyncSession):
        db_objs = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id,
            ),
        )
        return db_objs.scalars().all()

    async def get_by_subject_and_user_id(
            self,
            user_id: int,
            subject: SubjectEnum,
            session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id,
                self.model.subject == subject
            ),
        )
        return db_obj.scalars().first()

    async def create_score(
        self,
        user_id: int,
        subject: SubjectEnum,
        score: int,
        session: AsyncSession
    ) -> Score:
        db_obj = Score(user_id=user_id, subject=subject, score=score)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update_score(
        self,
        db_obj: Score,
        score: int,
        session: AsyncSession
    ) -> Score:
        db_obj.score = score
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


score_crud = ScoreCRUD(Score)
