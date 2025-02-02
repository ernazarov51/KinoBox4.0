from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

ikb_main = InlineKeyboardBuilder()
ikb_main.add(InlineKeyboardButton(text="Test", callback_data="test"))

admin_main_ikb = InlineKeyboardBuilder()
admin_main_ikb.add(InlineKeyboardButton(text="🍿 Kinolar", callback_data="adminkino"))
admin_main_ikb.add(InlineKeyboardButton(text="👤 Foydalanuvchilar", callback_data="adminuserdeeds"), )
admin_main_ikb.add(InlineKeyboardButton(text="like user", callback_data="login_like_user"))

admin_kino_ikb = InlineKeyboardBuilder()
admin_kino_ikb.add(InlineKeyboardButton(text="🎥 Kinolar royxati", switch_inline_query_current_chat='admin-kinolar'))
admin_kino_ikb.add(InlineKeyboardButton(text="⬆️🎞️ Kino qo'shish", callback_data="adminqosh"))
admin_kino_ikb.add(InlineKeyboardButton(text="🗑️ Kino O'chirish", callback_data="adminoch"))
admin_kino_ikb.add(InlineKeyboardButton(text="📊 Statistika", callback_data="statistika_kino"))
admin_kino_ikb.add(InlineKeyboardButton(text="↩️ orqaga", callback_data="adminback"))
admin_kino_ikb.adjust(2, 2, 1)

kino_qosh_stop_ikb = InlineKeyboardBuilder()
kino_qosh_stop_ikb.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="kino_qosh_otmen"))

conf_ikb = InlineKeyboardBuilder()
conf_ikb.add(InlineKeyboardButton(text="✅ Saqlash", callback_data='tasdiqlash'),
             InlineKeyboardButton(text="❌ Bekor qilish", callback_data='bekor'))
conf_ikb.adjust(2)

back_kb = InlineKeyboardBuilder()
back_kb.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data='orqaga'))

admin_user_main_ikb = InlineKeyboardBuilder()
admin_user_main_ikb.add(InlineKeyboardButton(text="📊 Statistika", callback_data="user_stat"),
                        InlineKeyboardButton(text="🔒 Bloklash", callback_data='user_blok'),
                        InlineKeyboardButton(text="📥 Murojaatlar", callback_data='messages'),
                        InlineKeyboardButton(text="👥 A'zolar", switch_inline_query_current_chat='admin-users'),
                        InlineKeyboardButton(text="🔐 Unblock", callback_data="unblock"),
                        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adminback"),

                        )
admin_user_main_ikb.adjust(3, 2, 1)

users_admin_back_ikb = InlineKeyboardBuilder()
users_admin_back_ikb.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data='review_back'))

user_choice_ikb = InlineKeyboardBuilder()
user_choice_ikb.add(InlineKeyboardButton(text="👥 A'zolar", switch_inline_query_current_chat='admin-users'))

kino_och = InlineKeyboardBuilder()
kino_och.add(InlineKeyboardButton(text="🆔 Kinolar", switch_inline_query_current_chat='admin-kinolar'))
kino_och.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data='orqaga'))

# =========user===============

user_start_ikb = InlineKeyboardBuilder()
user_start_ikb.add(
    InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data='settings'),
    InlineKeyboardButton(text="Media", callback_data='media'),
)

user_main_ikb = InlineKeyboardBuilder()
user_main_ikb.add(InlineKeyboardButton(text='🔍 Qidiruv', callback_data='qidirish'),
                  InlineKeyboardButton(text="🎥 Kinolar", switch_inline_query_current_chat='films'),
                  InlineKeyboardButton(text="🆕 Yangi kinolar", switch_inline_query_current_chat='last-added'),
                  InlineKeyboardButton(text="🎬 Janrlar Ro'yxati", callback_data='genre_list'),
                  InlineKeyboardButton(text="🏆 Hafta filmi", callback_data='week-film'),
InlineKeyboardButton(
        text="⬅️ Orqaga", callback_data='main_back')
                  )
user_main_ikb.adjust(2, 2, 1,1)

genres_ikb = InlineKeyboardBuilder()
genres_ikb.add(
    InlineKeyboardButton(text='Jangari 🗡️', switch_inline_query_current_chat='jangari'),
    InlineKeyboardButton(text='Fantastika ✨', switch_inline_query_current_chat='fantastika'),
    InlineKeyboardButton(text='Komediya 😂', switch_inline_query_current_chat='komediya'),
    InlineKeyboardButton(text='Drama 🎭', switch_inline_query_current_chat='drama'),
    InlineKeyboardButton(text='Triller 🔪', switch_inline_query_current_chat='triller'),
    InlineKeyboardButton(text='Sarguzasht 🗺️', switch_inline_query_current_chat='sarguzasht'),
    InlineKeyboardButton(text='Qo‘rqinchli 👻', switch_inline_query_current_chat='qo‘rqinchli'),
    InlineKeyboardButton(text='Tarixiy 🏰', switch_inline_query_current_chat='tarixiy'),
    InlineKeyboardButton(text='Biografik 📖', switch_inline_query_current_chat='biografik'),
    InlineKeyboardButton(text='Oilaviy 👨‍👩‍👧‍👦', switch_inline_query_current_chat='oilaviy'),
    InlineKeyboardButton(text='Animatsiya 🎨', switch_inline_query_current_chat='animatsiya'),
    InlineKeyboardButton(text='Detektiv 🔍', switch_inline_query_current_chat='detektiv'),
    InlineKeyboardButton(text="🎌🐉 Anime", switch_inline_query_current_chat='anime'),
    InlineKeyboardButton(
        text="⬅️ Orqaga", callback_data='genre_back')

)

genres_ikb.adjust(2, 3, 2, 3, 2, 1,1)

next_state = InlineKeyboardBuilder()
next_state.add(InlineKeyboardButton(text="❌", callback_data='next'))

user_back_ikb = InlineKeyboardBuilder()
user_back_ikb.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data='user_bekor'))

settings_ikb = InlineKeyboardBuilder()
settings_ikb.add(InlineKeyboardButton(text="My Data", callback_data='mydata'),
                 InlineKeyboardButton(text="👨‍💻 Adminga murojaat", callback_data='appeal'),
                 InlineKeyboardButton(text="⬅️ Back",callback_data='user_settings_back'))

settings_ikb.adjust(2,1)

settings_back_ikb = InlineKeyboardBuilder()
settings_back_ikb.add(InlineKeyboardButton(text="❌ Bekor qilish",callback_data='admin_apeal_back'))

# user_genre_back_ikb = InlineKeyboardBuilder()
# user_genre_back_ikb.add(InlineKeyboardButton(
#     text="⬅️ Orqaga", callback_data='genre_back')
# )
