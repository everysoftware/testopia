from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.db import Database
from .commands import BOT_COMMANDS_STR
from ..fsm import MainGroup
from ..keyboards.main import MAIN_MENU_KB
from ..middlewares import DatabaseMd

router = Router(name='main')

router.message.middleware(DatabaseMd())


@router.message(Command('start'))
async def start(
        message: types.Message,
        state: FSMContext,
        db: Database
) -> Message:
    await state.clear()

    async with db.session.begin():
        user_exists = await db.user.get(message.from_user.id) is not None

        if user_exists:
            sent_msg = await message.answer(
                f'Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}! 😊',
                reply_markup=MAIN_MENU_KB
            )
        else:
            sent_msg = await message.answer(
                f'Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}! '
                'Я помогаю тестировщикам организовывать задачи проекта. Давай приступим к работе! 😊',
                reply_markup=MAIN_MENU_KB
            )

            db.user.new(
                user_id=message.from_user.id,
                first_name=message.from_user.first_name,
                language_code=message.from_user.language_code,
                last_name=message.from_user.last_name,
                username=message.from_user.username
            )

        await state.set_state(MainGroup.viewing_menu)

        return sent_msg


@router.message(Command('help'))
async def help_(message: types.Message) -> Message:
    return await message.answer('<b>Способности бота:</b>\n\n' + BOT_COMMANDS_STR)


@router.message(Command('about'))
async def about(message: types.Message) -> Message:
    authors = ['@ApexBis', '@Dmitry_Skarga', '@ivanstasevich', '@midnightknight']

    return await message.answer(
        'Бот разработан специально для всероссийского конкурса <b>Студент года. IT</b>!\n\n'
        '👨‍💻: ' + ', '.join(authors)
    )
