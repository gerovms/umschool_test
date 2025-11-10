from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    first_name = State()
    surname = State()


class ChooseSubjectState(StatesGroup):
    subject = State()
    score = State()
