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
        [InlineKeyboardButton(text="📝 Список часто поставлених запитань", callback_data="menu")]
    ]
    )
    return ikb


def answer_list_ikb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❓Що відправити для пропуску", callback_data="first")],
        [InlineKeyboardButton(text="❓Маршрут на вигрузку", callback_data="second")],
        [InlineKeyboardButton(text="❓Маршрут на погрузку", callback_data="third")],
        [InlineKeyboardButton(text="❓Де брати документи на завантаження", callback_data="four")],
        [InlineKeyboardButton(text="❓Не працює навігація", callback_data="five")],
        [InlineKeyboardButton(text="🆘 Мені потрібна допомога зв'язок AI", callback_data="connect_ai")],
        [InlineKeyboardButton(text="↩ ️Назад", callback_data="back_main")]
    ]
    )
    return ikb


def back_list():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад", callback_data="menu")]
    ]
    )
    return ikb


def get_exit_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Завершити чат з AI")],
            [KeyboardButton(text="☎️ Складне питання", url="https://t.me/")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard
