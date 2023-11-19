from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.products import ProductGroup
from src.bot.handlers.products.show import show
from src.db import Database

router = Router()


@router.callback_query(F.data == 'add', MainGroup.viewing_products)
async def name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        'Назовите продукт. Например, VK Android App'
    )
    await state.set_state(ProductGroup.adding_product)

    await call.answer()


@router.message(ProductGroup.adding_product)
async def add(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        db.product.new(
            owner_id=message.from_user.id,
            name=message.text
        )

    await message.answer('Продукт успешно создан!')
    await show(message, state, db)
