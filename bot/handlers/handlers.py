import asyncio
from aiogram import Dispatcher, F, Bot
from aiogram.types import CallbackQuery, Message, InlineQuery, InlineQueryResultCachedVideo, \
    InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.buttons.inline import admin_kino_ikb, admin_main_ikb, conf_ikb, back_kb, admin_user_main_ikb, \
    kino_qosh_stop_ikb, users_admin_back_ikb, user_choice_ikb, user_back_ikb, user_main_ikb, kino_och, settings_ikb, \
    genres_ikb, next_state, user_start_ikb, settings_back_ikb
from bot.buttons.reply import create_button, code
from bot.handlers.functions import kino_statistics, search_users, search_movies, return_messages, block_user, \
    unblock_user, user_statistics, search_movie, last_added, search_genre, week_film, get_user_data, \
    generate_unique_code
from db.models import Models
from db.service import CRUD
from datetime import datetime


# ============== for user =========================
class SearchState(StatesGroup):
    input_code = State()


class AppealState(StatesGroup):
    input_message = State()


# ============== for user =========================


class SetMovie(StatesGroup):
    kod_input = State()
    title_input = State()


class BlockState(StatesGroup):
    userid_input = State()


class UnBlockState(StatesGroup):
    userid_input = State()


class DeleteMovie(StatesGroup):
    kino_input = State()


class AddMovie(StatesGroup):
    video = State()
    kod = State()
    title = State()
    description = State()
    genre = State()
    try_genre = State()
    year = State()
    language = State()
    country = State()
    age_border = State()
    form_end = State()


class AddGenre(StatesGroup):
    input_genre = State()


async def register_handler(dp: Dispatcher, bot: Bot):
    genres = "Jangari,Fantastika,Komediya,Drama,Triller,Sarguzasht,Qo‘rqinchli,Tarixiy,Biografik,Oilaviy,Animatsiya,Detektiv"
    current_genres=[]

    @dp.callback_query()
    async def process_callback(callback: CallbackQuery, state: FSMContext):
        data = callback.data
        chat_id = callback.message.chat.id

        # ============== for user =========================
        if data == 'mydata':
            caption = await get_user_data(user_id=str(callback.message.chat.id))
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=InputMediaPhoto(
                    media="AgACAgIAAxkBAAIOw2c-wpM17a1WvYGmu6YOxlIlZueAAAKY4jEbLZz4SbcOj309I-9rAQADAgADbQADNgQ",
                    caption=caption
                ),
                reply_markup=settings_back_ikb.as_markup()
            )
        if data == 'qidirish':
            await bot.send_message(chat_id=chat_id,text="Kino kodini yuboring", reply_markup=user_back_ikb.as_markup())
            await state.set_state(SearchState.input_code)

        if data == 'user_bekor':
            await state.clear()
            await bot.edit_message_text(chat_id=chat_id,message_id=callback.message.message_id, text="Assalomu Alaykum", reply_markup=user_main_ikb.as_markup())

        if data == 'appeal':
            await state.set_state(AppealState.input_message)
            await bot.send_message(chat_id=chat_id, text="📝")
            await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id, text="Adminga yubormoqchi bo'lgan xabaringizni yozing:",
                                   reply_markup=settings_back_ikb.as_markup())

        elif data == 'settings':
            await bot.edit_message_text(chat_id=chat_id,message_id=callback.message.message_id,text="Settings", reply_markup=settings_ikb.as_markup())

        elif data == 'genre_list':
            await bot.edit_message_text(chat_id=chat_id,message_id=callback.message.message_id,text="Janrlar Ro'yxati:", reply_markup=genres_ikb.as_markup())

        elif data == 'media':
            await bot.edit_message_text(message_id=callback.message.message_id,text="Salom", chat_id=callback.message.chat.id, reply_markup=user_main_ikb.as_markup())

        elif data == 'genre_back':
            await bot.edit_message_text(message_id=callback.message.message_id,text="⬅️", chat_id=callback.message.chat.id,
                                   reply_markup=user_main_ikb.as_markup())

        elif data=='main_back':
            await bot.edit_message_text(
                text="⬅️",
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=user_start_ikb.as_markup()
            )

        elif data=='user_settings_back':
            await bot.edit_message_text(message_id=callback.message.message_id,text="Salom", chat_id=callback.message.chat.id, reply_markup=user_start_ikb.as_markup()
                                   )

        elif data=='admin_apeal_back':
            await bot.send_message(text="Salom", chat_id=callback.message.chat.id,reply_markup=settings_ikb.as_markup())

        elif data == 'week-film':
            movie = await week_film()
            if movie:
                caption = f"""🎬 Nomi: {movie.title} 

🎥 Film
📅 Yili: {movie.year}
🇺🇿 Tili: {movie.language}
🎞 Janri: {movie.genre}

🎞️ Film kodi: {movie.film_code}
👁 Qidirilgan: {movie.visit_count} marta
🪓Yaqinlarga ulashing : @MediaUSAbot
     """
                await bot.send_video(chat_id=chat_id, video=movie.film, caption=caption)

        # ================Genre Handler==========
        # elif data=='jangari':

        # ============== for user =========================

        if data == 'next':
            await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id,text="janrlar saqlanishi uchun ixtioriy tugmani bosing")
            await state.set_state(AddMovie.try_genre)

        if data == 'unblock':
            msg = await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id, text="⚠️ Blokdan chiqarish uchun User tanlang:",
                                         reply_markup=user_choice_ikb.as_markup())
            await state.set_state(UnBlockState.userid_input)

        elif data == 'user_blok':
            msg = await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id, text="⚠️ Bloklash uchun User tanlang:",
                                         reply_markup=user_choice_ikb.as_markup())
            await state.set_state(BlockState.userid_input)

        elif data == "messages":
            msg = await return_messages()
            review = await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id, text=msg, reply_markup=users_admin_back_ikb.as_markup())
        elif data == "review_back":

            await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id, text="Quyidagilardan tanlang:",
                                   reply_markup=admin_user_main_ikb.as_markup())

        elif data == "test":
            await callback.message.answer("HI")
        elif data == "adminkino":

            await bot.edit_message_text(chat_id=chat_id,message_id=callback.message.message_id,text="Kinolar holatiga o'tdingiz.", reply_markup=admin_kino_ikb.as_markup())


        elif data == "tasdiqlash":
            data = await state.get_data()
            created_at = datetime.now()
            existing_movie = CRUD(Models.Movie).select_by_filter(film=data['video_id'])
            existing_kod = CRUD(Models.Movie).select_by_filter(film_code=data['kod'])
            if existing_movie:
                await callback.message.reply(
                    f"❌ Bu video allaqachon qo'shilgan. Film code: {existing_movie.film_code}")

            elif existing_kod:

                await callback.message.reply(
                    f"❌ Bu koddan avval foydalanilgan. Film: {existing_kod.title}")
            else:
                try:
                    CRUD(Models.Movie).add(
                        film=data['video_id'],
                        film_code=data['kod'],
                        title=data['title'],
                        description=data['description'],
                        genre=data['genre'],
                        year=data['year'],
                        language=data['language'],
                        country=data['country'],
                        age_border=data['age_border'],
                        created_at=created_at,
                        thumbnail="NONE",
                        visit_count=0,
                        added_by=callback.message.from_user.id

                    )
                    await callback.message.reply("Kino muvafaqqiyatli saqlandi 🟢")
                except Exception as e:
                    await callback.message.reply(f"Xato yuz berdi: {str(e)}")


        elif data == 'bekor':
            msg = await callback.message.reply("Bekor qilindi ❌")
            await callback.message.delete()
            await asyncio.sleep(5)
            await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)

        elif data == 'adminqosh':
            msg0 = await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id, text="✅ Kino qo'shish bo'limi",
                                          reply_markup=kino_qosh_stop_ikb.as_markup())
            msg_ = await bot.send_message(chat_id=chat_id, text="Kino ni jo'nating?")
            await state.set_state(AddMovie.video)

        elif data=='login_like_user':
            await callback.message.reply(text="Hello",reply_markup=user_main_ikb.as_markup())

        elif data == 'kino_qosh_otmen':
            await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id, text="Kinolar holatiga o'tdingiz.",
                                   reply_markup=admin_kino_ikb.as_markup())


            await state.clear()

        elif data == 'adminoch':
            await bot.edit_message_text(message_id=callback.message.message_id,chat_id=chat_id, text="O'chirmoqchi bo'lgan kinoni tanlashingiz mumkin",
                                   reply_markup=kino_och.as_markup())
            await state.set_state(DeleteMovie.kino_input)
        elif data == "adminback":
            await bot.edit_message_text(chat_id=chat_id,message_id=callback.message.message_id,text="Ishni boshlash uchun quidagilardan birini tanlang",
                                          reply_markup=admin_main_ikb.as_markup())
            await state.clear()
        elif data == 'orqaga':
            await bot.delete_message(message_id=callback.message.message_id,chat_id=chat_id,
                                   )
            await state.clear()






        elif data == "statistika_kino":
            caption = await kino_statistics()
            if caption:
                await bot.send_photo(chat_id=chat_id,
                                     photo="AgACAgIAAyEFAASMBnA7AAM1ZxxuXRYVazLJMzUllHHPxc7hjUoAAq3dMRtOdOlICTJBpHe9H6kBAAMCAAN4AAM2BA",
                                     caption=caption, reply_markup=back_kb.as_markup())
            else:
                await bot.send_photo(chat_id=chat_id,
                                     photo="AgACAgIAAyEFAASMBnA7AAMSZxiK4haLg_qKRz9GNYYzy7u4LDUAApnkMRuR0slIXkyYVtrU3mABAAMCAAN4AAM2BA",
                                     caption="Umumiy kinolar soni: ", reply_markup=back_kb.as_markup())
        elif data == "user_stat":
            await callback.message.delete()
            caption = await user_statistics()
            if caption:
                await bot.send_photo(chat_id=chat_id,
                                     photo="AgACAgIAAyEFAASMBnA7AAM1ZxxuXRYVazLJMzUllHHPxc7hjUoAAq3dMRtOdOlICTJBpHe9H6kBAAMCAAN4AAM2BA",
                                     caption=caption, reply_markup=users_admin_back_ikb.as_markup())
            else:
                await bot.send_photo(chat_id=chat_id,
                                     photo="AgACAgIAAyEFAASMBnA7AAMSZxiK4haLg_qKRz9GNYYzy7u4LDUAApnkMRuR0slIXkyYVtrU3mABAAMCAAN4AAM2BA",
                                     caption="Umumiy kinolar soni: ", reply_markup=users_admin_back_ikb.as_markup())


        elif data == 'adminuserdeeds':
            await bot.edit_message_text(chat_id=chat_id,message_id=callback.message.message_id,text="Quyidagilardan tanlang:", reply_markup=admin_user_main_ikb.as_markup())


    @dp.message(DeleteMovie.kino_input)
    async def delete_movie(message: Message, state: FSMContext):
        if message.caption:
            message_lines = message.caption.split('\n')
            film_code = message_lines[7][15:]
            CRUD(Models.Movie).delete(film_code=film_code)
            await bot.send_message(chat_id=message.chat.id, text="Kino Muvaffaqqiyatli o'chirildi!")

    @dp.inline_query(lambda query: query.query.startswith((
            'animes',
            'jangari',
            'fantastika',
            'komediya',
            'drama',
            'triller',
            'sarguzasht',
            'qo‘rqinchli',
            'tarixiy',
            'biografik',
            'oilaviy',
            'animatsiya',
            'detektiv'
    )))
    async def inline_users(inline_query: InlineQuery):
        title = inline_query.query
        results = await search_genre(title=title)
        if results:
            video_results = []

            for index, movie in enumerate(results, start=1):
                video_result = InlineQueryResultCachedVideo(
                    id=str(index),
                    video_file_id=movie.film,
                    title=movie.title,
                    description=f"""🎥Kino 👁{movie.age_border}
#{movie.genre}
                                """,
                    caption=f"""🐉Nomi: {movie.title}
🎥Tili: {movie.language}

🪓Chopar kanal : @MediaUSAbot
             """
                )
                video_results.append(video_result)

            await inline_query.answer(video_results, cache_time=1, is_personal=True)
        else:
            await inline_query.answer(
                results=[],  # Bo'sh ro'yxat yuborish
                switch_pm_text="Hech narsa topilmadi",
                switch_pm_parameter="no_results",  # Qo'shimcha parametr
                cache_time=1,
                is_personal=True
            )

    @dp.inline_query(lambda query: query.query.startswith('last-added'))
    async def inline_query_handler(inline_query: InlineQuery):
        title = inline_query.query
        results = await last_added(title=title)
        if results:

            video_results = []

            for index, movie in enumerate(results, start=1):
                video_result = InlineQueryResultCachedVideo(
                    id=str(index),
                    video_file_id=movie.film,
                    title=movie.title,
                    description=f"""🎥Kino 👁{movie.age_border}
    {movie.genre}
                        """,
                    caption=f"""🎬 Nomi: {movie.title} 

     🎥 Film
     📅 Yili: {movie.year}
     🇺🇿 Tili: {movie.language}
     🎞 Janri: {movie.genre}

     🎞️ Film kodi: {movie.film_code}
     🪓Yaqinlarga ulashing : @MediaUSAbot
     """
                )
                video_results.append(video_result)

            await inline_query.answer(video_results, cache_time=1, is_personal=True)
        else:
            await inline_query.answer(
                results=[],  # Bo'sh ro'yxat yuborish
                switch_pm_text="Hech narsa topilmadi",
                switch_pm_parameter="no_results",  # Qo'shimcha parametr
                cache_time=1,
                is_personal=True
            )

    @dp.inline_query(lambda query: query.query.startswith('admin-kinolar'))
    async def inline_query_handler(inline_query: InlineQuery):
        title = inline_query.query
        results = await search_movies(title=title)
        if results:

            video_results = []

            for index, movie in enumerate(results, start=1):
                video_result = InlineQueryResultCachedVideo(
                    id=str(index),
                    video_file_id=movie.film,
                    title=movie.title,
                    description=f"""🎥Kino 👁{movie.age_border}
{movie.genre}
                    """,
                    caption=f"""🎬 Nomi: {movie.title} 
                    
 🎥 Film
 📅 Yili: {movie.year}
 🇺🇿 Tili: {movie.language}
 🎞 Janri: {movie.genre}
 
 🎞️ Film kodi: {movie.film_code}
 🪓Chopar kanal : @MediaUSAbot
 """
                )
                video_results.append(video_result)

            await inline_query.answer(video_results, cache_time=1, is_personal=True)
        else:
            await inline_query.answer(
                results=[],  # Bo'sh ro'yxat yuborish
                switch_pm_text="Hech narsa topilmadi",
                switch_pm_parameter="no_results",  # Qo'shimcha parametr
                cache_time=1,
                is_personal=True
            )

    @dp.inline_query(lambda query: query.query.startswith('films'))
    async def inline_query_handler(inline_query: InlineQuery):
        title = inline_query.query
        results = await search_movies(title=title)
        if results:

            video_results = []

            for index, movie in enumerate(results, start=1):
                video_result = InlineQueryResultCachedVideo(
                    id=str(index),
                    video_file_id=movie.film,
                    title=movie.title,
                    description=f"""🎥Kino 👁{movie.age_border}
    {movie.genre}
                        """,
                    caption=f"""🎬 Nomi: {movie.title} 

     🎥 Film
     📅 Yili: {movie.year}
     🇺🇿 Tili: {movie.language}
     🎞 Janri: {movie.genre}

     🎞️ Film kodi: {movie.film_code}
     🪓Chopar kanal : @MediaUSAbot
     """
                )
                video_results.append(video_result)

            await inline_query.answer(video_results, cache_time=1, is_personal=True)
        else:
            await inline_query.answer(
                results=[],  # Bo'sh ro'yxat yuborish
                switch_pm_text="Hech narsa topilmadi",
                switch_pm_parameter="no_results",  # Qo'shimcha parametr
                cache_time=1,
                is_personal=True
            )

    @dp.inline_query(lambda query: query.query.startswith('admin-users'))
    async def inline_users(inline_query: InlineQuery):
        title = inline_query.query
        results = await search_users(title)
        users = []
        for index, user in enumerate(results, start=1):
            users_result = InlineQueryResultArticle(
                id=str(index),
                title=user.first_name,
                description=f"""👤 @{user.user_name}
{"🔴blocked" if user.is_blockes == 'true' else "🟢unblocked"}
{user.user_id}""",
                input_message_content=InputTextMessageContent(
                    message_text=f"""
🌟 **Foydalanuvchi ma'lumotlari** 🌟

➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
👤 Ism: {user.first_name}
📛 Foydalanuvchi nomi: @{user.user_name}
🆔 ID: {user.id}
🔔 Obuna bo'lganmi: {'✅ Ha' if not user.is_follow else "❌ Yo'q"}
🔐 Bloklanganmi: {'✅ Ha' if user.is_blockes == 'true' else "❌ Yo'q"}
📅 Yaratilgan sanasi: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}
👑 Administratormi: {'✅ Ha' if user.is_admin == 'true' else "❌ Yo'q"}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
""",
                    parse_mode='HTML'
                ),
            )
            users.append(users_result)
        await inline_query.answer(users, cache_time=1, is_personal=True)



    @dp.message(AddMovie.video)
    async def video(message: Message, state: FSMContext):
        try:
            await state.update_data(video_id=message.video.file_id)

            thumbnail_file_id = None
            if message.video.thumb and isinstance(message.video.thumb, dict):
                thumbnail_file_id = message.video.thumb.get('file_id')

            mesg1 = await bot.send_message(
                text="Kino kodini kiriting:",
                chat_id=message.chat.id,
                reply_markup=code.as_markup()
            )

            if thumbnail_file_id:
                await state.update_data(thumbnail_file_id=thumbnail_file_id)


            await state.set_state(AddMovie.kod)
        except Exception as e:
            ms = await message.reply("Iltimos Kino jonating ❗️")

            print(f"Error in video handler: {e}")

    @dp.message(AddMovie.kod)
    async def kod(message: Message, state: FSMContext):
        await state.update_data(kod=message.text)
        msgg = await message.reply("Kino nomini kiriting:")
        await state.set_state(AddMovie.title)

    @dp.message(AddMovie.title)
    async def description(message: Message, state: FSMContext):
        await state.update_data(title=message.text)
        msg2 = await message.reply("Kinoni qisqacha tariflang:")
        await state.set_state(AddMovie.description)

    @dp.message(AddMovie.description)
    async def genre(message: Message, state: FSMContext):
        await state.update_data(description=message.text)
        msg3 = await message.reply(
            "Kino janri qanday",
            reply_markup=await create_button(genres, '2'))

        await state.set_state(AddMovie.genre)
        print(message.text)



    @dp.message(AddMovie.genre)
    async def year(message: Message, state: FSMContext):
        genre=message.text
        current_genres.append(genre)
        await bot.send_message(chat_id=message.chat.id,text="Yana Janr Tanlashingiz mumkin",reply_markup=next_state.as_markup())
        msg4 = await message.reply("Yana janr tanlang")


    @dp.message(AddMovie.try_genre)
    async def year(message: Message, state: FSMContext):
        print(True)
        text = ''
        for i in current_genres:
            text += f'#{i}'
            text += ' '
        await state.update_data(genre=text)
        current_genres.clear()
        msg4 = await message.reply("Kino chiqqan yil:")
        await state.set_state(AddMovie.year)

    @dp.message(AddMovie.year)
    async def language(message: Message, state: FSMContext):
        await state.update_data(year=message.text)
        msg5 = await message.reply("Trjima tilini kiriting:",reply_markup=await create_button("Ingliz tilida,Rus tilida,O'zbek tilida",'2,1'))
        await state.set_state(AddMovie.language)

    @dp.message(AddMovie.language)
    async def country(message: Message, state: FSMContext):
        await state.update_data(language=message.text)
        msg6 = await message.reply("Kino davlatini kiritng:",reply_markup=await create_button('AQSH,UZB,Rossiya,Britaniya,Hindiston,Xitoy,Koreya,Yaponiya,Aniqlanmadi','2,2,2,2,1'))
        await state.set_state(AddMovie.country)

    @dp.message(AddMovie.country)
    async def age_border(message: Message, state: FSMContext):
        await state.update_data(country=message.text)
        msg7 = await message.reply("Yosh chegarasi:",reply_markup=await create_button('0,12,16,18','2,2'))

        await state.set_state(AddMovie.age_border)

    @dp.message(SetMovie.kod_input)
    async def kod_input(message: Message, state: FSMContext):

        try:
            kod = message.text
            CRUD(Models.Movie).delete(film_code=kod)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            msg = await message.reply("Kino Muvaffaqiyatli o'chirildi 🟢")
            await asyncio.sleep(5)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            await state.clear()
        except:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            msg = await message.reply("Topilmadi ❌")
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await asyncio.sleep(5)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            await state.clear()

    @dp.message(SetMovie.title_input)
    async def title_input(message: Message, state: FSMContext):
        try:
            title = message.text
            CRUD(Models.Movie).delete(title=title)
            msg = await message.reply("Kino Muvaffaqiyatli o'chirildi 🟢")
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id - 1)
            await asyncio.sleep(3)
            await msg.delete()
            await state.clear()
        except:
            msg = await message.reply("Topilmadi ❌")
            chat_id = message.chat.id
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await asyncio.sleep(3)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
            await state.clear()

    @dp.message(AddMovie.age_border)
    async def last(message: Message, state: FSMContext):
        films = CRUD(Models.Movie).select_all()
        await state.update_data(age_border=message.text)
        data = await state.get_data()
        film_code = data.get("video_id")
        caption = f"""
🍿 Kino nomi: {data['title']}
🎭 Janr: {data['genre']}
🗺 Til: {data['language']}
📆 Yuklangan sana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
‼️ Ko'rish chegarasi: {data['age_border']}

📥  | KODI: <<kod>>
🤖  | BIZNING BOT: @e_english_bot
"""
        await bot.send_video(chat_id=message.chat.id, video=film_code, caption=caption,
                             reply_markup=conf_ikb.as_markup())
        await state.set_state(AddMovie.form_end)

    @dp.message(F.text == "🔄 Boshiga qaytish")
    async def qaytish(message: Message, state: FSMContext):
        await state.clear()
        await bot.send_message(text=f"Ishni boshlash uchun quidagilardan birini tanlang",
                               chat_id=message.chat.id,
                               reply_markup=admin_main_ikb.as_markup())

    @dp.message(F.text == "🗒 Foydalanish qo'llanmasi")
    async def qollanma(message: Message, state: FSMContext):
        await state.clear()
        await message.reply("Hozircha qo'llanma yaratilmagan!")

    @dp.message(BlockState.userid_input)
    async def user_blocked(message: Message, state: FSMContext):

        message_rows = message.text.split('\n')
        if len(message_rows) > 3:
            user_id = int(message_rows[5][6])
            user = CRUD(Models.User).select_by_filter(id=user_id)
            if user.is_blockes == 'false':
                await block_user(id=user_id)
                text = f"🟢 {user.first_name} Muvaffaqqiyatli bloklandi!" if not user.user_name else f"🟢 @{user.user_name} Muvaffaqqiyatli bloklandi!"
                await state.clear()
            else:
                text = f"🔴 {user.first_name} Allaqachon bloklangan!" if not user.user_name else f"🔴 @{user.user_name} Allaqachon bloklangan!"
                await state.clear()
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            msg = await message.reply(text)
            await asyncio.sleep(5)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        else:
            await state.clear()
            await message.reply("Yana bir bor kiriting")

        # user_id ni msg dan kesib olish va fuctions.user_block(user_id)

    @dp.message(UnBlockState.userid_input)
    async def user_unblocked(message: Message, state: FSMContext):

        message_rows = message.text.split('\n')
        if len(message_rows) > 3:
            user_id = int(message_rows[5][6])
            user = CRUD(Models.User).select_by_filter(id=user_id)
            if user.is_blockes == 'true':
                await unblock_user(id=user_id)
                text = f"🟢 {user.first_name} Muvaffaqqiyatli blokdan chiqarildi!" if not user.user_name else f"🟢 @{user.user_name} Muvaffaqqiyatli blokdan chiqarildi!"
                await state.clear()
            else:
                text = f"🔴 {user.first_name} Blokda emas!" if not user.user_name else f"🔴 @{user.user_name} Blokda emas!"
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            msg = await message.reply(text)
            await asyncio.sleep(5)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)


        else:
            await state.clear()
            await message.reply("Yana bir bor kiriting")

    @dp.message(F.photo)
    async def send_image_code(message: Message):
        await bot.send_message(chat_id=-1002349232187, text=f"Photo ID: {message.photo[-1].file_id}")

    @dp.message(F.video)
    async def send_video_code(message: Message):
        await bot.send_message(chat_id=-1002349232187, text=f"Video ID: {message.video.file_id}")

    # =============== for user ===============

    @dp.message(F.text == "🔍 Kino qidirsh")
    async def kin_qidirsh(message: Message, state: FSMContext):
        await state.clear()
        await message.reply("Bosh Menyu", reply_markup=user_main_ikb.as_markup())

    @dp.message(F.text == "🗒Foydalanuvchi qo'llanmasi")
    async def kin_qidirsh(message: Message, state: FSMContext):
        await state.clear()
        await message.reply("Foydalanuvchi qo'llanmasi topilmadi.")

    @dp.message(SearchState.input_code)
    async def search_movie_handler(message: Message, state: FSMContext):
        code = message.text
        movie = await search_movie(code=code)
        if movie:
            caption = f"""
🍿 Kino nomi: {movie.title}
🎭 Janr: {movie.genre}
🗺 Til: {movie.language}
📆 Yuklangan sana: {str(movie.created_at)[:-7]}
‼️ Ko'rish chegarasi: {movie.age_border}

📥  | KODI: {movie.film_code}
🤖  | BIZNING BOT: @e_english_bot
                """
            await bot.send_video(chat_id=message.chat.id, video=movie.film, caption=caption)
            await state.clear()
        else:
            await message.reply("Topilmadi ⚠️\\nKodni qaytadan yuboring!", reply_markup=user_back_ikb.as_markup())

    @dp.message(AppealState.input_message)
    async def appeal_handler(message: Message, state: FSMContext):
        message_to_admin = message.text
        CRUD(Models.Review).add(review=message_to_admin, user_id=message.from_user.id)
        await message.reply("Xabaringiz adminga yuborildi.")
        await state.clear()
