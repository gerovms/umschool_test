from typing import Any, List

from core.db import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mp

from utils.constants import NAME_LENGTH


class User(Base):

    __tablename__ = "users"

    first_name: Mapped[str] = mp(String(NAME_LENGTH), nullable=False)
    surname: Mapped[str] = mp(String(NAME_LENGTH), nullable=False)
    tg_id: Mapped[int] = mp(
        Integer,
        unique=True,
        index=True,
        nullable=True,
    )

    scores: Mapped[List["Score"]] = relationship(
        "Score", back_populates="user", cascade="all, delete-orphan"
    )
