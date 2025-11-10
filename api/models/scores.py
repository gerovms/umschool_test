from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column as mp, relationship

from core.db import Base
from core.enums import SubjectEnum
from models.users import User


class Score(Base):
    __tablename__ = "scores"

    user_id: Mapped[int] = mp(ForeignKey("users.id", ondelete="CASCADE"))
    subject: Mapped[SubjectEnum] = mp(
        ENUM(SubjectEnum, name="subjectenum", create_type=False),
        nullable=False
    )
    score: Mapped[int] = mp(Integer, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="scores")

    __table_args__ = (
        UniqueConstraint("user_id", "subject", name="uq_user_subject"),
        CheckConstraint("score >= 0 AND score <= 100", name="ck_score_range"),
    )
