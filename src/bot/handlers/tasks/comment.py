from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.tasks import TaskGroup
from src.bot.handlers.tasks.show_one import show_task
from src.bot.keyboards.service import CANCEL_KB
from src.db import Database
from src.db.models import Comment

router = Router()


@router.callback_query(F.data == "comment", MainGroup.viewing_task)
async def text(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Введите новый комментарий", reply_markup=CANCEL_KB)
    await state.set_state(TaskGroup.editing_comment)

    await call.answer()


@router.message(TaskGroup.editing_comment)
async def edit_comment(message: types.Message, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        task = await db.task.get(user_data["task_id"])
        comment: Comment = task.comment

        if comment is None:
            task.comment = db.comment.new(text=message.text)
            await db.task.merge(task)
        else:
            comment.text = message.text
            await db.comment.merge(comment)

    await message.answer("Комментарий успешно обновлён!")

    await show_task(message, state, db, user_data["task_id"])
