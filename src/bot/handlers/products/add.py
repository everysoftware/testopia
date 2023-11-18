from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.products import ProductGroup
from src.bot.handlers.activities import AddProductActivity
from src.bot.handlers.products.show import show
from src.db import Database

router = Router(name='products_add')


@router.callback_query(F.data == 'add', MainGroup.viewing_products)
async def add(call: types.CallbackQuery, state: FSMContext) -> None:
    await AddProductActivity.start_callback(
        call, state,
        new_state=ProductGroup.adding_product,
        text='Назовите продукт. Например, VK Mobile App'
    )


@router.message(ProductGroup.adding_product)
async def type_name(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        db.product.new(
            owner_id=message.from_user.id,
            name=message.text
        )

    await AddProductActivity.finish(
        message, state,
        text='Продукт успешно создан!'
    )

    await show(message, state, db)
