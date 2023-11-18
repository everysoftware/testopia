from aiogram.fsm.state import StatesGroup, State


class DeviceGroup(StatesGroup):
    adding_device = State()
