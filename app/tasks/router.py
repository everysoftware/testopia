import datetime
import os

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from app.checklists.dependencies import ChecklistServiceDep
from app.checklists.states import ChecklistGroup
from app.db.schemas import PageParams
from app.db.types import ID
from app.db.utils import naive_utc
from app.keyboards import CANCEL_KB
from app.tasks.constants import TASK_STATUSES
from app.tasks.dependencies import TaskServiceDep
from app.tasks.keyboards import get_tasks_kb, SHOW_TASK_KB, EDIT_TASK_STATUS_KB
from app.tasks.states import TaskGroup
from app.users.dependencies import MeDep

router = Router()


# GET MANY
@router.callback_query(F.data == "to_checklist")
@router.callback_query(F.data.startswith("show_"), ChecklistGroup.get_many)
async def get_many(
    event: types.CallbackQuery | types.Message,
    state: FSMContext,
    service: TaskServiceDep,
    checklist_service: ChecklistServiceDep,
    *,
    checklist_id: ID | None = None,
) -> None:
    if isinstance(event, types.CallbackQuery):
        message = event.message
        if event.data.startswith("show_"):
            checklist_id = int(event.data.split("_")[1])
        else:
            user_data = await state.get_data()
            checklist_id = user_data["checklist_id"]
    else:
        message = event
    assert checklist_id is not None

    response = await service.get_many(checklist_id, PageParams(limit=100))
    kb = get_tasks_kb(response)
    checklist = await checklist_service.get_one(checklist_id)

    cap = (
        f"🗒 Чек-лист {checklist.name}\n\n"
        f"Продукт: {checklist.product}\n"
        f"Создан: {checklist.created_at}\n"
        f"Изменен: {checklist.updated_at}\n\n"
    )
    if response.total > 0:
        await message.answer(cap + "Задачи:", reply_markup=kb)
    else:
        await message.answer(cap + "Нет задач", reply_markup=kb)

    await state.update_data(checklist_id=checklist_id)
    await state.set_state(TaskGroup.get_many)
    if isinstance(event, types.CallbackQuery):
        await event.answer()


# CREATE
@router.callback_query(F.data == "add", TaskGroup.get_many)
async def get_name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Назовите задачу. Например, `протестировать регистрацию`",
        reply_markup=CANCEL_KB,
    )
    await state.set_state(TaskGroup.enter_name)
    await call.answer()


@router.message(TaskGroup.enter_name)
async def create(
    message: types.Message,
    state: FSMContext,
    user: MeDep,
    service: TaskServiceDep,
    checklist_service: ChecklistServiceDep,
) -> None:
    user_data = await state.get_data()
    checklist_id = user_data["checklist_id"]
    name = message.text
    await service.create(checklist_id=checklist_id, user_id=user.id, name=name)
    await message.answer("Задача успешно создана!")

    await get_many(
        message, state, service, checklist_service, checklist_id=checklist_id
    )


# GET
@router.callback_query(F.data.startswith("show_"), TaskGroup.get_many)
async def get(
    event: types.CallbackQuery | types.Message,
    state: FSMContext,
    service: TaskServiceDep,
    checklist_service: ChecklistServiceDep,
    task_id: ID | None = None,
) -> None:
    if isinstance(event, types.CallbackQuery):
        message = event.message
        task_id = int(event.data.split("_")[1])
    else:
        message = event
        assert task_id is not None

    task = await service.get_one(task_id)
    report_url = task.report_url if task.report_url else "нет"
    comment = task.comment if task.comment else "нет"

    user_data = await state.get_data()
    checklist_id = user_data["checklist_id"]
    checklist = await checklist_service.get_one(checklist_id)

    await message.answer(
        f"📌 *Задача: {task.name}*\n\n"
        f"Статус: {TASK_STATUSES[task.status]["text"]} {TASK_STATUSES[task.status]["emoji"]}\n"
        f"Чек-лист: {checklist.name}\n"
        f"Отчёт об ошибках: {report_url}\n"
        f"Комментарий: {comment}\n"
        f"Создана: {task.created_at}\n"
        f"Изменена: {task.updated_at}",
        reply_markup=SHOW_TASK_KB,
    )

    await state.set_state(TaskGroup.get)
    await state.update_data(task_id=task_id)
    if isinstance(event, types.CallbackQuery):
        await event.answer()


# EDIT REPORT
@router.callback_query(F.data == "report", TaskGroup.get)
async def enter_url(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Введите ссылку на отчёт об ошибках")
    await state.set_state(TaskGroup.enter_report_url)
    await call.answer()


@router.message(TaskGroup.enter_report_url)
async def edit_report(
    message: types.Message,
    state: FSMContext,
    checklist_service: ChecklistServiceDep,
    service: TaskServiceDep,
) -> None:
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, report_url=message.text)
    await message.answer("Ссылка на отчёт об ошибках успешно обновлена!")

    await get(message, state, service, checklist_service, task_id=task_id)


# EDIT STATUS
@router.callback_query(F.data == "edit", TaskGroup.get)
async def enter_status(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Выберите новый статус задачи", reply_markup=EDIT_TASK_STATUS_KB
    )
    await state.set_state(TaskGroup.enter_status)
    await call.answer()


@router.callback_query(F.data.startswith("set_"), TaskGroup.enter_status)
async def edit_status(
    call: types.CallbackQuery,
    state: FSMContext,
    checklist_service: ChecklistServiceDep,
    service: TaskServiceDep,
) -> None:
    new_status = call.data.split("_")[1]
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, status=new_status)
    await call.message.answer("Статус задачи успешно изменен!")
    await get(call.message, state, service, checklist_service, task_id=task_id)

    await call.answer()


# EDIT COMMENT
@router.callback_query(F.data == "comment", TaskGroup.get)
async def text(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Введите новый комментарий")
    await state.set_state(TaskGroup.enter_comment)
    await call.answer()


@router.message(TaskGroup.enter_comment)
async def edit_comment(
    message: types.Message,
    state: FSMContext,
    checklist_service: ChecklistServiceDep,
    service: TaskServiceDep,
) -> None:
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, comment=message.text)
    await message.answer("Комментарий успешно обновлен!")

    await get(message, state, service, checklist_service, task_id=task_id)


# STATS


@router.message(Command("stats"))
@router.message(F.text == "Статистика 📊")
async def show(
    message: types.Message, user: MeDep, service: TaskServiceDep
) -> None:
    status_stats_path = await service.plot_by_statuses(user.id)
    try:
        await message.answer_photo(
            photo=FSInputFile(status_stats_path),
            caption="Статистика за все время",
        )
    finally:
        os.remove(status_stats_path)

    now = naive_utc()
    daily_stats_path = await service.plot_by_days(
        user.id, now, now - datetime.timedelta(days=365)
    )
    try:
        await message.answer_photo(
            photo=FSInputFile(daily_stats_path),
            caption="Пройденные тесты за последний год",
        )
    finally:
        os.remove(daily_stats_path)
