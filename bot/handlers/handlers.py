import aiohttp
from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils.enums import SubjectEnum

from keyboards import keyboards as kb
from messages import messages as m
from states import states as s
from utils import constants as c
from utils import validators as v

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(m.GREETINGS)


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await message.answer(m.FIRST_NAME_MESSAGE)
    await state.set_state(s.RegisterState.first_name)


@router.message(F.text, StateFilter(s.RegisterState.first_name))
async def type_surname(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer(m.SURNAME_MESSAGE)
    await state.set_state(s.RegisterState.surname)


@router.message(F.text, StateFilter(s.RegisterState.surname))
async def registration_end(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()
    await state.clear()
    data["tg_id"] = int(message.from_user.id)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{c.API_URL}/register",
            json=data
        ):
            await message.answer(m.REGISTRATION_END_MESSAGE)


@router.message(Command("enter_scores"))
async def cmd_enter_scores(message: Message, state: FSMContext):
    await message.answer(
        m.CHOOSE_SUBJECT,
        reply_markup=await kb.build_subjects_keyboard()
        )
    await state.set_state(s.ChooseSubjectState.subject)


@router.callback_query(F.data.startswith('page:'))
async def change_page(callback: CallbackQuery):
    page = int(callback.data.split(':')[1])
    await callback.message.edit_text(
        text=m.CHOOSE_SUBJECT,
        reply_markup=await kb.build_subjects_keyboard(page)
    )
    await callback.answer()


@router.callback_query(
        F.data.in_([s.name for s in SubjectEnum]),
        StateFilter(s.ChooseSubjectState.subject)
        )
async def process_subject(callback: CallbackQuery, state: FSMContext):
    subject = callback.data
    await state.update_data(subject=SubjectEnum[subject].value)
    await callback.message.answer(m.TYPE_SCORE)
    await state.set_state(s.ChooseSubjectState.score)


@router.message(F.text, StateFilter(s.ChooseSubjectState.score))
async def process_score(message: Message, state: FSMContext):
    try:
        score = int(message.text)
        await v.validate_scores(score)
    except ValueError:
        await message.answer(m.WRONG_SCORE)
        return
    await state.update_data(score=int(score))
    data = await state.get_data()
    data["tg_id"] = int(message.from_user.id)
    await state.clear()
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{c.API_URL}/scores", json=data):
            await message.answer(m.SCORE_END_MESSAGE)


@router.message(Command("view_scores"))
async def cdm_view_scores(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{c.API_URL}/scores/{message.from_user.id}"
        ) as resp:
            if resp.status != 200:
                await message.answer(m.NO_REGISTRATION)
                return
            data = await resp.json()
            if not data.get("scores"):
                await message.answer(m.NO_SCORES)
                return
            msg = "\n".join(
                f"{s['subject']} – {s['score']}" for s in data["scores"]
                )
            await message.answer(f"Ваши баллы:\n{msg}")
