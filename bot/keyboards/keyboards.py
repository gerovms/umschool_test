from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.enums import SubjectEnum

from utils.constants import SUBJECTS_PER_PAGE, TOTAL_PAGES


async def build_subjects_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    subjects = list(SubjectEnum)
    start_idx = page * SUBJECTS_PER_PAGE
    end_idx = start_idx + SUBJECTS_PER_PAGE
    page_items = subjects[start_idx:end_idx]

    keyboard = []
    for subj in page_items:
        keyboard.append(
            [InlineKeyboardButton(
                text=subj.value,
                callback_data=subj.name
            )]
        )

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data=f'page:{page - 1}'
        ))
    if page < TOTAL_PAGES - 1:
        nav_buttons.append(InlineKeyboardButton(
            text='Вперёд ➡️',
            callback_data=f'page:{page + 1}'
        ))
    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
