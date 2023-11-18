from aiogram.fsm.state import StatesGroup, State


class ProductGroup(StatesGroup):
    adding_product = State()
