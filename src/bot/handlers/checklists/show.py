from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.keyboards.checklists import get_checklist_kb
from src.db import Database

router = Router()


async def show_checklists(message: types.Message, state: FSMContext, db: Database, product_id: int) -> None:
    await state.update_data(product_id=product_id)

    async with db.session.begin():
        product = await db.product.get(product_id)
        kb = await get_checklist_kb(product.checklists)

    if len(kb.inline_keyboard) == 1:
        await message.answer(f'У Вас нет чек-листов для продукта <b>{product.name}</b>', reply_markup=kb)
    else:
        await message.answer(f'Ваши чек-листы для продукта <b>{product.name}</b>', reply_markup=kb)

    await state.set_state(MainGroup.viewing_checklists)


@router.callback_query(F.data.startswith('show_'), MainGroup.viewing_products)
async def show(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    product_id = int(call.data.split('_')[1])

    await show_checklists(call.message, state, db, product_id)

    await call.answer()
