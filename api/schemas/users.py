from pydantic import BaseModel, Field

from schemas.scores import ScoreOut
from utils.constants import NAME_LENGTH


class UserCreate(BaseModel):
    first_name: str = Field(..., max_length=NAME_LENGTH)
    surname: str = Field(..., max_length=NAME_LENGTH)
    tg_id: int


class UserOut(BaseModel):
    scores: list[ScoreOut] = []

    class Config:
        from_attributes = True
