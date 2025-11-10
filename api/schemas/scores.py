from pydantic import BaseModel, Field

from core.enums import SubjectEnum


class ScoreCreate(BaseModel):
    tg_id: int
    subject: SubjectEnum
    score: int = Field(..., ge=0, le=100)

    class Config:
        use_enum_values = True


class ScoreOut(BaseModel):
    subject: SubjectEnum
    score: int

    class Config:
        from_attributes = True
