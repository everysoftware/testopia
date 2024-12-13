import logging

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from app.base.types import UUID as ID, UUID
from app.bot import bot
from app.projects import router as projects_router
from app.projects.dependencies import ProjectServiceDep
from app.tasks.constants import TASK_STATUSES, TEST_STATUSES
from app.tasks.dependencies import TaskServiceDep
from app.tasks.keyboards import (
    SHOW_TASK_KB,
    EDIT_TASK_STATUS_KB,
    EDIT_TEST_STATUS_KB,
)
from app.tasks.schemas import TaskStatus, TestStatus
from app.tasks.states import TaskGroup
from app.users.dependencies import UserDep
from app.utils import sanitize_markdown, split_message

router = Router()


# CREATE
@router.callback_query(F.data == "add", TaskGroup.get_many)
async def get_name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Назовите задачу. Например, `добавить авторизацию`"
    )
    await state.set_state(TaskGroup.enter_name)
    await call.answer()


@router.message(TaskGroup.enter_name)
async def create(
    message: types.Message,
    state: FSMContext,
    user: UserDep,
    service: TaskServiceDep,
    project_service: ProjectServiceDep,
) -> None:
    user_data = await state.get_data()
    project_id = user_data["project_id"]
    workspace_id = user_data["workspace_id"]
    name = message.text
    await service.create(
        workspace_id=workspace_id,
        project_id=project_id,
        user_id=user.id,
        name=name,
    )
    await message.answer("Задача успешно создана!")

    await projects_router.get(
        message, state, service, project_service, project_id=project_id
    )


# GET
@router.callback_query(F.data.startswith("show_task:"), TaskGroup.get_many)
async def get(
    event: types.CallbackQuery | types.Message,
    state: FSMContext,
    service: TaskServiceDep,
    project_service: ProjectServiceDep,
    task_id: ID | None = None,
) -> None:
    user_data = await state.get_data()

    if isinstance(event, types.CallbackQuery):
        message = event.message
        task_id = UUID(event.data.split(":")[1])
    else:
        message = event
        if task_id is None:
            task_id = user_data["task_id"]
    assert task_id is not None

    task = await service.get_one(task_id)
    report_url = task.report_url if task.report_url else "нет"
    desc = task.description if task.description else "нет"

    project_id = user_data["project_id"]
    project = await project_service.get_one(project_id)

    await message.answer(
        f"📌 Задача: *{task.name}*\n\n"
        f"Проект: {project.name}\n"
        f"Статус: {TASK_STATUSES[task.status]["text"]} {TASK_STATUSES[task.status]["emoji"]}\n"
        f"Описание: {desc}\n"
        f"Тест: {TEST_STATUSES[task.test_status]["text"]} {TEST_STATUSES[task.test_status]["emoji"]}\n"
        f"Отчёт: {report_url}\n"
        f"Создано: {task.created_at}\n"
        f"Изменено: {task.updated_at}",
        reply_markup=SHOW_TASK_KB,
    )

    await state.set_state(TaskGroup.get)
    await state.update_data(task_id=str(task_id))
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
    project_service: ProjectServiceDep,
    service: TaskServiceDep,
) -> None:
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, report_url=message.text)
    await message.answer("Ссылка на отчёт об ошибках успешно обновлена!")
    await get(message, state, service, project_service, task_id=task_id)


# EDIT STATUS
@router.callback_query(F.data == "edit_status", TaskGroup.get)
async def enter_status(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Выберите новый статус задачи", reply_markup=EDIT_TASK_STATUS_KB
    )
    await state.set_state(TaskGroup.enter_status)
    await call.answer()


@router.callback_query(
    F.data.startswith("set_status:"), TaskGroup.enter_status
)
async def edit_status(
    call: types.CallbackQuery,
    state: FSMContext,
    project_service: ProjectServiceDep,
    service: TaskServiceDep,
) -> None:
    new_status = call.data.split(":")[1]
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, status=new_status)
    await call.message.answer("Статус задачи успешно изменен!")
    await get(call.message, state, service, project_service, task_id=task_id)
    await call.answer()


# EDIT TEST STATUS
@router.callback_query(F.data == "edit_test_status", TaskGroup.get)
async def enter_test_status(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    await call.message.answer(
        "Выберите новый статус теста", reply_markup=EDIT_TEST_STATUS_KB
    )
    await state.set_state(TaskGroup.enter_status)
    await call.answer()


@router.callback_query(
    F.data.startswith("set_test_status:"), TaskGroup.enter_status
)
async def edit_test_status(
    call: types.CallbackQuery,
    state: FSMContext,
    project_service: ProjectServiceDep,
    service: TaskServiceDep,
) -> None:
    test_status = call.data.split(":")[1]
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    if test_status != TestStatus.no_status:
        await service.update(
            task_id, status=TaskStatus.done, test_status=test_status
        )
    else:
        await service.update(task_id, test_status=test_status)
    await call.message.answer("Статус теста успешно изменен!")
    await get(call.message, state, service, project_service, task_id=task_id)
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
    project_service: ProjectServiceDep,
    service: TaskServiceDep,
) -> None:
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    await service.update(task_id, description=message.text)
    await message.answer("Комментарий успешно обновлен!")

    await get(message, state, service, project_service, task_id=task_id)


@router.callback_query(F.data == "complete", TaskGroup.get)
async def solve(
    call: types.CallbackQuery,
    state: FSMContext,
    service: TaskServiceDep,
) -> None:
    await call.answer()
    await bot.send_chat_action(call.message.chat.id, "typing")
    user_data = await state.get_data()
    task_id = user_data["task_id"]
    full_text = await service.solve(task_id)
    full_text = sanitize_markdown(full_text)
    logging.info("Full_text: %s", full_text)
    for part in split_message(full_text):
        await call.message.answer(part, parse_mode="HTML")
