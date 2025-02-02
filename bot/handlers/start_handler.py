import asyncio
import datetime

from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.buttons.reply import create_button
from aiogram.types import Message, CallbackQuery
from db.service import CRUD
from db.models import Models
from utils.config import CF as conf
from bot.buttons.inline import ikb_main, admin_main_ikb, user_main_ikb, user_start_ikb
from aiogram.fsm.state import State, StatesGroup
from bot.buttons.reply import create_button


class StartState(StatesGroup):
    begin = State()


async def start_register(dp: Dispatcher, bot):
    @dp.message(CommandStart())

    async def start(message: Message, state: FSMContext):
        print(message.from_user.id)
        await state.clear()
        user = CRUD(Models.User).select_by_filter(user_id=str(message.from_user.id))
        if str(message.from_user.id) not in conf.Admins.Admins.split(','):
            if not user:
                CRUD(Models.User).add(user_name=message.from_user.username, first_name=message.from_user.first_name,
                                      user_id=message.from_user.id, created_at=datetime.datetime.now())
                await bot.send_message(text="Yana bir marta /start ni bosing)", chat_id=message.chat.id,
                                       reply_markup=await create_button("/start", "1"))
            elif user.is_blockes != 'true':
                await bot.send_message(text="Salom", chat_id=message.chat.id,reply_markup=user_start_ikb.as_markup()
                                       )
            else:
                await bot.send_message(text="🔴 Kechirasiz Siz Blok Holatidasiz", chat_id=message.chat.id,
                                       )
        else:
            user = CRUD(Models.User).select_by_filter(user_id=str(message.from_user.id))
            if not user:

                CRUD(Models.User).add(user_name=message.from_user.username, first_name=message.from_user.first_name,
                                      user_id=message.from_user.id, created_at=datetime.datetime.now(), is_admin='true')
                await message.answer(text="💻 Assalomu Alaykum, Siz Adminsiz! Admin Panel",
                                     reply_markup=await create_button("🔄 Boshiga qaytish,🗒 Foydalanish qo'llanmasi",
                                                                      '2'))

                await bot.send_message(text=f"Ishni boshlash uchun quidagilardan birini tanlang",
                                       chat_id=message.chat.id,
                                       reply_markup=admin_main_ikb.as_markup())
            else:
                await message.answer(text="💻 Assalomu Alaykum, Siz Adminsiz! Admin Panel",
                                     reply_markup=await create_button("🔄 Boshiga qaytish,🗒 Foydalanish qo'llanmasi",
                                                                      '2'))

                await bot.send_message(text=f"Ishni boshlash uchun quidagilardan birini tanlang",
                                       chat_id=message.chat.id,
                                       reply_markup=admin_main_ikb.as_markup())

    async def back_callback(callback: CallbackQuery, state: FSMContext):
        await state.set_state(StartState.begin)
        await bot.send_message(text=f"Ishni boshlash uchun quidagilardan birini tanlang",
                               reply_markup=admin_main_ikb.as_markup(), chat_id=callback.message.chat.id)
        await state.clear()
