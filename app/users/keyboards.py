from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

MAIN_MENU_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Мои задачи ✅"),
            KeyboardButton(text="Мои проекты 📝"),
        ],
        [
            KeyboardButton(text="Мои пространства 📦"),
            KeyboardButton(text="Статистика 📊"),
        ],
        [
            KeyboardButton(text="Навигация по боту 🧭"),
        ],
    ],
    resize_keyboard=True,
)
