from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.checklists.dependencies import ChecklistServiceDep
from app.checklists.keyboards import get_checklist_kb
from app.checklists.states import ChecklistGroup
from app.db.schemas import PageParams
from app.users.dependencies import MeDep

router = Router()


@router.message(Command("checklists"))
@router.message(F.text == "Мои чек-листы 📝")
async def get_many(
        message: types.Message, state: FSMContext, user: MeDep, service: ChecklistServiceDep
) -> None:
    response = await service.get_many(PageParams(limit=100), user_id=user.id)
    kb = get_checklist_kb(response)
    if response.total > 0:
        await message.answer("Чек-листы:", reply_markup=kb)
    else:
        await message.answer("Нет чек-листов", reply_markup=kb)
    await state.set_state(ChecklistGroup.get_many)


@router.callback_query(F.data == "add", ChecklistGroup.get_many)
async def enter_name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Назовите список задач. Например, `авторизация`"
    )
    await state.set_state(ChecklistGroup.enter_name)
    await call.answer()


@router.message(ChecklistGroup.enter_name)
async def enter_product(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        "Укажите продукт. Например, `VK Android App`"
    )
    await state.set_state(ChecklistGroup.enter_product)


@router.message(ChecklistGroup.enter_product)
async def add(message: types.Message, state: FSMContext, user: MeDep, service: ChecklistServiceDep) -> None:
    user_data = await state.get_data()
    name = user_data["name"]
    product = message.text
    await service.create(user_id=user.id, name=name, product=product)
    await message.answer("Список задач успешно создан!")
    await get_many(message, state, user, service)
