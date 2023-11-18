from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.tasks import TaskGroup
from src.bot.handlers.activities import AddTaskActivity
from src.bot.handlers.tasks.show import show_ as show_tasks
from src.db import Database

router = Router(name='tasks_add')


@router.callback_query(F.data == 'add', MainGroup.viewing_tasks)
async def add(call: types.CallbackQuery, state: FSMContext) -> None:
    await AddTaskActivity.start_callback(
        call, state,
        new_state=TaskGroup.adding_task,
        text='Назовите задачу. Например, протестировать аутентификацию'
    )


@router.message(TaskGroup.adding_task)
async def type_name(message: types.Message, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        db.task.new(
            user_id=message.from_user.id,
            task_list_id=user_data['task_list_id'],
            name=message.text
        )

    await AddTaskActivity.finish(
        message, state,
        text='Задача успешно создана!'
    )

    await show_tasks(message, state, db, user_data['task_list_id'])
