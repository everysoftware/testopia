from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.keyboards.task_lists import get_task_lists_kb
from src.db import Database

router = Router(name='task_lists_show')


async def show_(message: types.Message, state: FSMContext, db: Database, product_id: int) -> None:
    await state.update_data(product_id=product_id)

    async with db.session.begin():
        product = await db.product.get(product_id)
        kb = await get_task_lists_kb(product)

    if len(kb.inline_keyboard) == 1:
        await message.answer(f'У Вас нет чек-листов для <b>{product.name}</b>', reply_markup=kb)
    else:
        await message.answer(f'Ваши чек-листы для <b>{product.name}</b>', reply_markup=kb)

    await state.set_state(MainGroup.viewing_task_lists)


@router.callback_query(F.data.startswith('show_'), MainGroup.viewing_products)
async def show(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    product_id = int(call.data.split('_')[1])

    await show_(call.message, state, db, product_id)

    await call.answer()
