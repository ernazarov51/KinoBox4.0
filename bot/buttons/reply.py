from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder,KeyboardButton

from bot.handlers.functions import generate_unique_code


async def create_button(buttons_str: str, design: str):
    buttons=buttons_str.split(',')
    design=map(int,design.split(','))
    rkb=ReplyKeyboardBuilder()
    for i in buttons:
        rkb.add(KeyboardButton(text=i))
    rkb.adjust(*design)

    return rkb.as_markup(resize_keyboard=True)

code = ReplyKeyboardBuilder()
code.add(KeyboardButton(text=generate_unique_code()))
code.adjust(1)
code.one_time_keyboard = True
