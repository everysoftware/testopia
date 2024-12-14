from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.commands import BOT_COMMANDS_STR
from app.users.dependencies import UserServiceDep
from app.users.keyboards import MAIN_MENU_KB
from app.users.schemas import UserCreate

router = Router()


@router.message(CommandStart())
async def start_command(
    message: types.Message, state: FSMContext, users: UserServiceDep
) -> None:
    assert message.from_user
    user = await users.get_by_telegram_id(message.from_user.id)
    if not user:
        data = UserCreate(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        user = await users.register(state, data)
    await message.answer(
        f"Добро пожаловать, {user.display_name}! 😊",
        reply_markup=MAIN_MENU_KB,
    )


@router.message(Command("help"))
@router.message(F.text == "Навигация по боту 🧭")
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
