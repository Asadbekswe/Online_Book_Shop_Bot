from aiogram.fsm.state import StatesGroup, State


class CountState(StatesGroup):
    product_id = State()
    count = State()
