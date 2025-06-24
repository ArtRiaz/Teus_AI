from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# Keyboards

# New user
def start_keyboard_user():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="☀️ Авторизация", callback_data="auth")]
    ]
    )
    return ikb


def start_keyboard_user_db():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝Список часто поставлених запитань", callback_data="menu")]
    ]
    )
    return ikb


def answer_list_ikb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❓Де брати документи", callback_data="first")],
        [InlineKeyboardButton(text="❓Де завантаження", callback_data="second")],
        [InlineKeyboardButton(text="❓Куди мені їхати", callback_data="third")],
        [InlineKeyboardButton(text="❓Що потрібно відправити для пропуску", callback_data="four")],
        [InlineKeyboardButton(text="❓Не працює посилання на навігацію", callback_data="five")],
        [InlineKeyboardButton(text="🆘Мені потрібна допомога зв'язок AI", callback_data="connect_ai")],
        [InlineKeyboardButton(text="☎️Складне питання", callback_data="difficult_answer")],
        [InlineKeyboardButton(text="↩️Назад", callback_data="back_main")]
    ]
    )
    return ikb


def back_list():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️Назад", callback_data="menu")]
    ]
    )
    return ikb


def get_exit_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Завершити чат з AI")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard
