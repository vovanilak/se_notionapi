from aiogram.filters.state import State, StatesGroup

class Card(StatesGroup):
    who = State()
    row_as_test = State()
    row_vt_test = State()
    action = State()
    do = State()