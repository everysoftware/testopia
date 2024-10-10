from aiogram.fsm.state import StatesGroup, State


class DeviceGroup(StatesGroup):
    get_many = State()
    get = State()
    enter_name = State()
