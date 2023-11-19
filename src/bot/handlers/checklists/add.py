from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.checklists import ChecklistGroup
from src.bot.handlers.checklists.show import show_checklists as show_checklists
from src.db import Database

router = Router()


@router.callback_query(F.data == 'add', MainGroup.viewing_checklists)
async def name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Назовите список задач. Например, авторизация')
    await state.set_state(ChecklistGroup.adding_checklist)

    await call.answer()


@router.message(ChecklistGroup.adding_checklist)
async def add(message: types.Message, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        db.checklist.new(
            name=message.text,
            product_id=user_data['product_id']
        )

    await message.answer('Список задач успешно создан!')
    await show_checklists(message, state, db, user_data['product_id'])
