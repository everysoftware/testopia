from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.task_lists import TaskListGroup
from src.bot.handlers.activities import AddTaskListActivity
from src.bot.handlers.task_lists.show import show_ as show_task_lists
from src.db import Database

router = Router(name='task_lists_add')


@router.callback_query(F.data == 'add', MainGroup.viewing_task_lists)
async def add(call: types.CallbackQuery, state: FSMContext) -> None:
    await AddTaskListActivity.start_callback(
        call, state,
        new_state=TaskListGroup.adding_list,
        text='Назовите список задач. Например, юнит-тесты'
    )


@router.message(TaskListGroup.adding_list)
async def type_name(message: types.Message, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        db.task_list.new(
            name=message.text,
            product_id=user_data['product_id']
        )

    await AddTaskListActivity.finish(
        message, state,
        text='Список задач успешно создан!'
    )

    await show_task_lists(message, state, db, user_data['product_id'])
