from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from app.commands import BOT_COMMANDS_STR
from app.users.dependencies import UserServiceDep
from app.users.keyboards import MAIN_MENU_KB
from app.users.schemas import UserCreate

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message, users: UserServiceDep) -> None:
    assert message.from_user
    user = await users.get_by_telegram_id(message.from_user.id)
    if user:
        await message.answer(
            f"Добро пожаловать, {user.display_name}! 😊",
            reply_markup=MAIN_MENU_KB,
        )
    else:
        data = UserCreate(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        user = await users.register(data)
        await message.answer(
            f"Добро пожаловать, {user.display_name}! "
            "Я помогаю тестировщикам организовывать задачи проекта. Давай приступим к работе! 😊",
            reply_markup=MAIN_MENU_KB,
        )


@router.message(Command("help"))
@router.message(F.text == "Помощь 🆘")
async def get_help(message: types.Message) -> None:
    await message.answer("**Навигация по боту**:\n\n" + BOT_COMMANDS_STR)


@router.message(Command("about"))
async def about(message: types.Message) -> None:
    text = (
        "**Testopia** - мощный инструмент для ведения проектов.\n\n"
        "Поддерживает управление проектами, задачами и тестами.\n\n"
        "Используйте команду /help для получения списка доступных команд."
    )
    await message.answer(text)
