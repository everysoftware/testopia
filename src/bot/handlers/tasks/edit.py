from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm.task_lists import TaskListGroup
from src.bot.fsm.tasks import TaskGroup
from src.bot.handlers.activities import EditTaskActivity
from src.bot.keyboards.tasks import EDIT_TASK_STATUS_KB, TASK_STATES_CB_DATA
from src.db import Database
from .show import show_ as show_tasks

router = Router(name='tasks_edit')


@router.callback_query(F.data.startswith('edit_'), TaskListGroup.in_testing_session)
async def edit(call: types.CallbackQuery, state: FSMContext) -> None:
    task_id = int(call.data.split('_')[1])
    await state.update_data(task_id=task_id)

    await EditTaskActivity.start_callback(
        call, state,
        new_state=TaskGroup.editing_task_status,
        text='Выберите новый статус задачи',
        reply_markup=EDIT_TASK_STATUS_KB
    )


@router.callback_query(F.data.startswith('set_'), TaskGroup.editing_task_status)
async def select_status(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    new_task_state = TASK_STATES_CB_DATA[call.data.split('_')[1]]

    user_data = await state.get_data()

    async with db.session.begin():
        task = await db.task.get(user_data['task_id'])
        task.state = new_task_state
        await db.task.merge(task)

    await EditTaskActivity.finish_callback(
        call, state,
        new_state=TaskListGroup.in_testing_session,
        text='Статус задачи успешно изменен!',
    )

    await call.message.answer('Статус задачи успешно изменен!')
    await show_tasks(call.message, state, db, user_data['task_list_id'], True)
