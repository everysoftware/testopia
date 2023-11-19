from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm.checklists import ChecklistGroup
from src.bot.fsm.tasks import TaskGroup
from src.bot.keyboards.tasks import EDIT_TASK_STATUS_KB, TASK_STATES_CB_DATA
from src.db import Database
from .show import show_tasks as show_tasks

router = Router()


@router.callback_query(F.data.startswith('edit_'), ChecklistGroup.conducting_testing_session)
async def edit(call: types.CallbackQuery, state: FSMContext) -> None:
    task_id = int(call.data.split('_')[1])
    await state.update_data(task_id=task_id)

    await call.message.answer(
        'Выберите новый статус задачи',
        reply_markup=EDIT_TASK_STATUS_KB
    )
    await state.set_state(TaskGroup.editing_task_status)

    await call.answer()


@router.callback_query(F.data.startswith('set_'), TaskGroup.editing_task_status)
async def select_status(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    new_task_state = TASK_STATES_CB_DATA[call.data.split('_')[1]]

    user_data = await state.get_data()

    async with db.session.begin():
        task = await db.task.get(user_data['task_id'])
        task.state = new_task_state
        await db.task.merge(task)

    await call.message.answer('Статус задачи успешно изменен!')
    await state.set_state(ChecklistGroup.conducting_testing_session)

    await show_tasks(call.message, state, db, user_data['checklist_id'], True)

    await call.answer()
