from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from app.tasks.constants import TASK_STATUS_CB_DATA
from app.tasks.states import TaskGroup
from app.database import Database
from .show_one import show_task
from ...fsm import MainGroup
from app.tasks.keyboards import EDIT_TASK_STATUS_KB

router = Router()


@router.callback_query(F.data == "edit", MainGroup.viewing_task)
async def edit(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Выберите новый статус задачи", reply_markup=EDIT_TASK_STATUS_KB
    )
    await state.set_state(TaskGroup.editing_task_status)

    await call.answer()


@router.callback_query(F.data.startswith("set_"), TaskGroup.editing_task_status)
async def select_status(
    call: types.CallbackQuery, state: FSMContext, db: Database
) -> None:
    new_task_state = TASK_STATUS_CB_DATA[call.data.split("_")[1]]

    user_data = await state.get_data()

    async with db.session.begin():
        task = await db.task.get(user_data["task_id"])
        task.status = new_task_state
        await db.task.merge(task)

    await call.message.answer("Статус задачи успешно изменен!")

    await show_task(
        call.message,
        state,
        db,
        user_data["task_id"],
    )

    await call.answer()
