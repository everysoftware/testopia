from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.tasks import TaskGroup
from src.bot.handlers.tasks.show import show_tasks as show_tasks
from src.db import Database

router = Router()


@router.callback_query(F.data == 'add', MainGroup.viewing_tasks)
async def name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        'Назовите задачу. Например, протестировать регистрацию'
    )
    await state.set_state(TaskGroup.adding_task)

    await call.answer()


@router.message(TaskGroup.adding_task)
async def add(message: types.Message, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        db.task.new(
            user_id=message.from_user.id,
            checklist_id=user_data['checklist_id'],
            name=message.text
        )

    await message.answer('Задача успешно создана!')

    await show_tasks(message, state, db, user_data['checklist_id'])
