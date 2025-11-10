from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from core.db import get_async_session
from core.enums import SubjectEnum
from crud.scores import score_crud
from crud.users import user_crud
from models.users import User
from schemas.scores import ScoreCreate, ScoreOut
from schemas.users import UserCreate, UserOut

router = APIRouter()


@router.post(
    "/register",
    response_model=UserOut,
    status_code=HTTPStatus.CREATED,
)
async def create_user(
    obj_in: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        user: User = await user_crud.create(obj_in, session)
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@router.post(
    "/scores",
    response_model=ScoreOut,
    status_code=HTTPStatus.CREATED,
)
async def write_score(
    obj_in: ScoreCreate,
    session: AsyncSession = Depends(get_async_session),
):
    if isinstance(obj_in.subject, str):
        try:
            obj_in.subject = SubjectEnum[obj_in.subject]
        except KeyError:
            obj_in.subject = SubjectEnum(obj_in.subject)
    user = await user_crud.get_by_tg_id(obj_in.tg_id, session)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Пользователь не найден. Сначала зарегистрируйтесь."
        )
    existing_score = await score_crud.get_by_subject_and_user_id(
        user.id,
        obj_in.subject,
        session
    )
    if existing_score:
        return await score_crud.update_score(
            existing_score,
            obj_in.score,
            session
            )
    else:
        return await score_crud.create_score(user.id,
                                             obj_in.subject,
                                             obj_in.score,
                                             session
                                             )


@router.get(
    "/scores/{tg_id}",
    response_model=UserOut,
)
async def get_scores(
    tg_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get_by_tg_id(tg_id, session)
    if user:
        scores = await score_crud.get_by_user_id(user.id, session)
        return {"scores": scores}
    raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Пользователь не найден. Сначала зарегистрируйтесь."
        )
