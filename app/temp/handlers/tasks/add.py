from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from app.bot.fsm import MainGroup
from app.tasks.states import TaskGroup
from app.bot.handlers.tasks.show import show_tasks as show_tasks
from app.keyboards import CANCEL_KB
from app.database import Database
from app.database.models import Task

router = Router()


@router.callback_query(F.data == "add", MainGroup.viewing_tasks)
async def name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Назовите задачу. Например, <code>протестировать регистрацию</code>",
        reply_markup=CANCEL_KB,
    )
    await state.set_state(TaskGroup.adding_task)

    await call.answer()


@router.message(TaskGroup.adding_task)
async def add(message: types.Message, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        checklist = await db.checklist.get(user_data["checklist_id"])
        task = Task(user_id=message.from_user.id, name=message.text)
        checklist.tasks.append(task)

    await message.answer("Задача успешно создана!")

    await show_tasks(message, state, db, user_data["checklist_id"])
