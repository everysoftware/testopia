from aiogram.fsm.state import StatesGroup, State


class ChecklistGroup(StatesGroup):
    get_many = State()
    enter_name = State()
    enter_product = State()
    get = State()
